#!/usr/bin/env python2.6
from __future__ import division

import multiprocessing, threading, time, socket, re, struct, hashlib, base64, copy

class LEDController(object):
    def __init__(self, device, framerate=30, start_websocket=True, \
                    ws_hostname='localhost', ws_orig_port=5000, ws_port=9999):
        
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
            self.add_writer(WebsocketWriter(framerate, ws_hostname, ws_orig_port, ws_port))
        
        self.queue_thread = threading.Thread(target=self.pump_queue)
        self.queue_thread.start()
            
    def get_current_pattern(self):
        return self.current_pattern
    
    def get_queue(self):
        return self.queue
    
    def set_pattern_rep_count(self, entry_id, num_times):
        self.queue_lock.acquire()
        for i in range(len(self.queue)):
            if id(self.queue[i]) == entry_id:
                self.queue[i][2] = num_times
                
        self.queue_lock.release()
    
    def remove_pattern(self, entry_id):
        self.queue_lock.acquire()
        for i in range(len(self.queue)):
            if id(self.queue[i]) == entry_id:
                self.queue.pop(index)
                break
        
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
        self.queue.append([name, pattern, num_times])
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
    
    def assert_writers_alive(self):
        for w in self.writers:
            if not w.is_alive():
                raise SystemExit
    
    def wait_for_data(self):
        while len(self.queue) == 0:
            self.queue_has_data.wait(0.1)
            self.assert_writers_alive();
    
    def wait_for_finish(self):
        for w in self.writers:
            w.wait_for_finish()
    
    def quit(self):
        self.add_pattern(None)
    
    def pump_queue(self):
        while True:
            self.wait_for_data()
            
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
            
            row_start = time.time()
            for frame in pattern:
                self.assert_writers_alive()
                
                if not self._play.is_set():
                    self._play.wait()
                
                if self._next.is_set():
                    self._next.clear()
                    return
                                
                self.draw_frame(frame)
                
                dt = time.time() - row_start
                if dt < self.frame_dt:
                    time.sleep(self.frame_dt - dt)
                # else:
                    # print 'Draw slow by %f sec' % (dt-self.frame_dt)
                
                row_start = time.time()
                
            count += 1
    
    def draw_frame(self, frame):
        for w in self.writers:
            w.send_frame(frame)
                    
class PatternWriter(multiprocessing.Process):
    
    def __init__(self, framerate):
        super(PatternWriter, self).__init__()
        
        self.frame_dt = 1.0 / framerate
    
    def open_port(self):
        raise NotImplementedError
    
    def draw_frame(self, frame):
        raise NotImplementedError
    
    def close_port(self):
        raise NotImplementedError
    
    def setup(self, pipe_in, pipe_out):
        self.pipe_in = pipe_in        # For use inside this process
        self.pipe_out = pipe_out        # For exterior use
    
    def send_frame(self, pattern_data):
        if not self.is_alive():
            raise SystemExit
        
        if self.pipe_out.poll():
            r = self.pipe_out.recv()
            if r.has_key('status') and r['status'] == 'exiting':
                raise SystemExit
            
        self.pipe_out.send(pattern_data)
    
    def run(self):
        self.open_port()
        try:
            while True:
                frame = self.pipe_in.recv()
                
                if frame is None:
                    raise SystemExit
                
                self.draw_frame(frame)
        
        except (KeyboardInterrupt, SystemExit):
            self.exit()
    
    def exit(self):
        print '\b\bExiting, please wait...'
        try:
            while self.pipe_in.poll():  # Empty buffers
                self.pipe_in.recv()
            self.pipe_in.send(dict(status='exiting'))
            self.pipe_in.close()
        except Exception, e:
            print 'Got exception on exit: ', e
        self.close_port()
        raise SystemExit

class WebsocketWriter(PatternWriter):
    
    def __init__(self, framerate, hostname, orig_port, port):
        super(WebsocketWriter, self).__init__(framerate)
        self.hostname = hostname
        self.orig_port = orig_port
        self.port = port

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
            print 'Accepted websocket connection from %s' % str(addr)
            header = ''
            while not re.search("\r\n\r\n", header): # Receive headers
                header += client.recv(1024)
                        
            key = re.search("Sec-WebSocket-Key: ([^\s]*)\s*$", header, re.M).group(1)
            
            s = key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
            respkey = base64.b64encode(hashlib.sha1(s).digest())
            resp = \
                "HTTP/1.1 101 Web Socket Protocol Handshake\r\n" + \
                "Upgrade: WebSocket\r\n" + \
                "Connection: Upgrade\r\n" + \
                "Sec-WebSocket-Accept: " + respkey + "\r\n" + \
                "\r\n"
                        
            client.send(resp)
            self.clients_lock.acquire()
            self.clients.append(client)
            self.clients_lock.release()
    
    def draw_frame(self, frame):
        json_frame = ['{"status":"ok", "frame" : [']
        
        for i in range(0, len(frame)-3, 3):
            r, g, b = frame[i:i+3]
            json_frame.extend(['"rgb(',str(r),',',str(g),',',str(b),')",'])
        
        r, g, b = frame[-3:]
        json_frame.extend(['"rgb(',str(r),',',str(g),',',str(b),')"]}'])
        # Fast string concatenation trick
        json_data = ''.join(json_frame)
        
        self.client_push(json_data)
        
    def client_push(self, data):
        self.clients_lock.acquire()
        dead_clients = []

        b1 = 0x80 | (0x01 & 0x0f) 
        payload_len = len(data)
        if payload_len <= 125:
            header = struct.pack('>BB', b1, payload_len)
        elif payload_len > 125 and payload_len < 65536:
            header = struct.pack('>BBH', b1, 126, payload_len)
        elif payload_len >= 65536:
            header = struct.pack('>BBQ', b1, 127, payload_len)
        
        for i in range(len(self.clients)):
            try:
                self.clients[i].send(header)
                self.clients[i].send(data)
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
