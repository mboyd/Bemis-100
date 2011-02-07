#!/usr/bin/env python2.6
from __future__ import division

import pattern
import multiprocessing, threading, time, socket, re, struct, hashlib

class LEDController:
    def __init__(self, device, framerate=30, start_websocket=True):
        self.frame_dt = 1.0 / framerate
        self.device = device
        
        self.writers = []
        
        if start_websocket:
            self.add_writer(WebsocketWriter(framerate))
    
    def add_writer(self, writer):
        self.writers.append(writer)
        writer.start()
    
    def add_pattern(self, pattern, num_times=-1, async=True):
        for w in self.writers:
            w.add_pattern(pattern, num_times)
        
        if not async:
            self.wait_for_finish()
    
    def play(self):
        for w in self.writers:
            w.play()
    
    def pause(self):
        for w in self.writers:
            w.pause()
    
    def is_playing(self):
        if len(self.writers) > 0:
            return self.writers[0].is_playing()
        else:
            return False
    
    def next(self):
        for w in self.writers:
            w.next()
    
    def wait_for_finish(self):
        for w in self.writers:
            w.wait_for_finish()
    
    def quit(self):
        self.add_pattern(None)
            
class PatternWriter(multiprocessing.Process):
    
    def __init__(self, framerate):
        super(PatternWriter, self).__init__()
        
        self.frame_dt = 1.0 / framerate
        
        self.play_queue = multiprocessing.JoinableQueue()
        
        self._play = multiprocessing.Event()    # Continue playing; if not set, enter pause mode, 
                                                # staying on the same pattern
        
        self._next = multiprocessing.Event()    # If set, skip to the next pattern
    
    def open_port(self):
        raise NotImplementedError
    
    def draw_frame(self, frame):
        raise NotImplementedError
    
    def close_port(self):
        raise NotImplementedError
    
    def add_pattern(self, pattern, num_times):
        self.play_queue.put_nowait((pattern, num_times))
    
    def play(self):
        self._play.set()
    
    def pause(self):
        self._play.clear()
    
    def is_playing(self):
        return self._play.is_set()
    
    def next(self):
        self._next.set()
    
    def wait_for_finish(self):
        if not self.is_alive():
            raise SystemExit
        self.play_queue.join()

    def run(self):
        self.open_port()
        try:
            while True:
                pattern, num_times = self.play_queue.get()
                
                if pattern is None:
                    raise SystemExit
                
                self.draw_pattern(pattern, num_times)
                self.play_queue.task_done()
        
        except (KeyboardInterrupt, SystemExit):
            self.exit()
    
    def exit(self):
        print 'Writer thread exiting'
        try:
            while self.play_queue.get_nowait():
                self.play_queue.task_done()
        except Exception:
            pass
        self.close_port()
        raise SystemExit
    
    def draw_pattern(self, pattern, num_times):
        count = 0
        while self._play.is_set():
            if (num_times > 0 and count == num_times):
                break
                        
            for frame in pattern:
                if not self._play.is_set():
                    self._play.wait()
                
                if self._next.is_set():
                    self._next.clear()
                    return
                                
                row_start = time.time()
                
                self.draw_frame(frame)
                
                dt = time.time() - row_start
                if dt < self.frame_dt:
                    time.sleep(self.frame_dt - dt)
            count += 1


class WebsocketWriter(PatternWriter):

    def open_port(self):
        self.clients = []
        self.clients_lock = threading.Lock()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.sock.bind(('', 9999))  
        self.sock.listen(1)
        
        self.connection_thread = threading.Thread(target=self.handle_connections)
        self.connection_thread.start()
    
    def handle_connections(self):
        while True:
            client, addr = self.sock.accept()
            print 'Accepted connection from %s' % str(addr)
            header = ''
            while not re.search("\r\n\r\n.{8}", header): # Receive headers + 8 bytes data
                header += client.recv(1024)
            
            key1 = re.search("Sec-WebSocket-Key1: (.*)$", header, re.M).group(1)
            key2 = re.search("Sec-WebSocket-Key2: (.*)$", header, re.M).group(1)
            
            data = header[-8:]
            
            key1n = int(re.sub("[^\d]", '', key1))
            key1ns = key1.count(' ')
            n1 = key1n // key1ns
            
            key2n = int(re.sub("[^\d]", '', key2))
            key2ns = key2.count(' ')
            n2 = key2n // key2ns
            
            s = struct.pack("!ii", n1, n2) + data
            respkey = hashlib.md5(s).digest()
            resp = \
                "HTTP/1.1 101 Web Socket Protocol Handshake\r\n" + \
                "Upgrade: WebSocket\r\n" + \
                "Connection: Upgrade\r\n" + \
                "Sec-WebSocket-Origin: http://localhost\r\n" + \
                "Sec-WebSocket-Location: ws://localhost:9999/\r\n" + \
                "Sec-WebSocket-Protocol: ledweb\r\n\r\n" + \
                respkey + "\r\n"
            
            client.send(resp)
            self.clients_lock.acquire()
            self.clients.append(client)
            self.clients_lock.release()
    
    def draw_frame(self, frame):
        json_frame = '{"status":"ok", "frame" : ['
        for i in range(0, len(frame), 3):
            r, g, b = map(pattern.decode_char, frame[i:i+3])
            json_frame += '"rgb(%i,%i,%i)",' % (r, g, b)
        json_frame = json_frame[:-1] + ']}'
        
        self.client_push(json_frame)
        
    def client_push(self, data):
        self.clients_lock.acquire()
        dead_clients = []
        for i in range(len(self.clients)):
            try:
                self.clients[i].send("\x00"+data+"\xff")
            except socket.error:
                dead_clients.append(i)
        
        for i in dead_clients:
            self.close_sock(self.clients[i])
            del self.clients[i]
        self.clients_lock.release()
    
    def close_port(self):
        self.client_push('{"status":"exiting"}')
        time.sleep(1.0)
        
        self.clients_lock.acquire()
        for c in self.clients:
            self.close_sock(c)
        self.clients_lock.release()
        self.close_sock(self.sock)
    
    def close_sock(self, s):
        try:
            c.shutdown(socket.SHUT_RDWR)
            c.close()
        except Exception:
            pass
