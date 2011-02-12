#!/usr/bin/env python2.6
from __future__ import division

import pattern
import multiprocessing, threading, time, socket, re, struct, hashlib, copy

class LEDController(object):
    def __init__(self, device, framerate=30, start_websocket=True):
        self.frame_dt = 1.0 / framerate
        self.device = device
        
        self.queue = []
        self.queue_has_data = threading.Event()
        self.queue_lock = threading.RLock()
        self.current_pattern = None
        
        self.writers = []
        self.writer_count = 0
        self.done_writer_count = 0
        
        self._play = threading.Event()    # Continue playing; if not set, enter pause mode, 
                                                # staying on the same pattern
        
        self._next = threading.Event()    # If set, skip to the next pattern
        
        if start_websocket:
            self.add_writer(WebsocketWriter(framerate))
        
        self.queue_thread = threading.Thread(target=self.pump_queue)
        self.queue_thread.start()
            
    def get_current_pattern(self):
        return self.current_pattern
    
    def get_queue(self):
        return self.queue
    
    def remove_pattern(self, index):
        self.queue_lock.acquire()
        self.queue.pop(index)
        if len(self.queue) == 0:
            self.queue_has_data.clear()
        self.queue_lock.release()
    
    def add_writer(self, writer):
        i, o = multiprocessing.Pipe()
        writer.setup(i, o)
        self.writers.append(writer)
        self.writer_count += 1
        writer.start()
    
    def add_pattern(self, pattern, num_times=-1, name='', async=True):
        self.queue_lock.acquire()
        self.queue.append((name, pattern, num_times))
        self.queue_has_data.set()
        self.queue_lock.release()
        
        if not async:
            self.wait_for_finish()
    
    def play(self):
        self._play.set()
    
    def pause(self):
        self._play.clear()
    
    def is_playing(self):
        return self._play.is_set()
    
    def next(self):
        self._next.set()
    
    def wait_for_finish(self):
        for w in self.writers:
            w.wait_for_finish()
    
    def quit(self):
        self.add_pattern(None)
    
    def pump_queue(self):
        while True:
            self.queue_has_data.wait()
            self.queue_lock.acquire()
            name, pattern, n = self.queue.pop(0)
            self.current_pattern = pattern
            self.queue_lock.release()
            
            self.draw_pattern(pattern, n)
    
    def draw_pattern(self, pattern, num_times):
        count = 0
        while True:
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
                else:
                    print 'Draw slow by %f sec' % (dt-self.frame_dt)
                
            count += 1
    
    def draw_frame(self, frame):
        for w in self.writers:
            w.send_frame(frame)
            
class PatternWriter(multiprocessing.Process):
    
    def __init__(self, framerate):
        super(PatternWriter, self).__init__()
        
        self.frame_dt = 1.0 / framerate
    
    def setup(self, pipe_in, pipe_out):
        self.pipe_in = pipe_in  # For use inside this process
        self.pipe_out = pipe_out    # For exterior use
    
    def open_port(self):
        raise NotImplementedError
    
    def draw_frame(self, frame):
        raise NotImplementedError
    
    def close_port(self):
        raise NotImplementedError
    
    def send_frame(self, pattern_data):
        self.pipe_out.send(pattern_data)
    
    def run(self):
        self.open_port()
        try:
            while True:
                frame = self.pipe_in.recv()
                
                if pattern is None:
                    raise SystemExit
                
                self.draw_frame(frame)
                #self.pipe_in.send(dict(status='done'))
        
        except (KeyboardInterrupt, SystemExit):
            self.exit()
    
    def exit(self):
        print 'Writer thread exiting'
        try:
            self.pipe_in.send(dict(status='exiting'))
            self.pipe_in.close()
        except Exception, e:
            print 'Got exception on exit: ', e
        self.close_port()
        raise SystemExit

class WebsocketWriter(PatternWriter):

    def open_port(self):
        self.clients = []
        self.clients_lock = threading.Lock()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            
            s = struct.pack("!II", n1, n2) + data
            respkey = hashlib.md5(s).digest()
            resp = \
                "HTTP/1.1 101 Web Socket Protocol Handshake\r\n" + \
                "Upgrade: WebSocket\r\n" + \
                "Connection: Upgrade\r\n" + \
                "Sec-WebSocket-Origin: http://localhost:5000\r\n" + \
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
        
        for i in range(len(dead_clients)):
            self.close_sock(self.clients[dead_clients[i]-i])
            del self.clients[dead_clients[i]-i]
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
