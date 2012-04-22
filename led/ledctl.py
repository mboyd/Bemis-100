#!/usr/bin/env python2.6
from __future__ import division

import multiprocessing, threading, time, socket, re, struct, hashlib, copy, base64, sys

class LEDController(object):
    def __init__(self, device, framerate=30, start_websocket=True, \
                    websocket=None):
        
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
        
        # if start_websocket:
        #     self.add_writer(WebsocketWriter(framerate, websocket))
        
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
    
    def clear_queue(self):
        self.queue_lock.acquire()
        for i in range(len(self.queue)):
            self.queue.pop(i)
        
        self.queue_has_data.clear()
        self.queue_lock.release()
    
    def add_writer(self, writer):
        i, o = multiprocessing.Pipe()
        writer.setup(i, o)
        self.writers.append(writer)
        self.writer_count += 1
        writer.start()
    
    def remove_writer(self, writer):
        writer.send_frame([])
    
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
                self.writers.remove(w)
                # raise SystemExit
    
    def wait_for_data(self):
        while len(self.queue) == 0:
            self.queue_has_data.wait(0.1)
            self.assert_writers_alive();
    
    def wait_for_finish(self):
        for w in self.writers:
            w.wait_for_finish()
    
    def quit(self):
        self.clear_queue()
        self.add_pattern([[]])
        if not self.is_playing():
            self.play()
        else:
            self.next()
    
    def pump_queue(self):
        while True:
            self.wait_for_data()
            
            self.queue_lock.acquire()
            name, pattern, n = self.queue.pop(0)
            self.current_pattern = {'pattern': pattern, 'name': name, 'num_times': n}
            self.queue_lock.release()
            
            if pattern is not None:
                self.draw_pattern(pattern, n)
            else:
                print "Controller exiting..."
                for w in self.writers:
                    w.exit()
    
    def draw_pattern(self, pattern, num_times):
        count = 0
        while True:
            if (num_times > 0 and count == num_times):
                break
            
            row_start = time.time()
            if pattern is None:
                self.exit()
            
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
                else:
                    print 'Draw slow by %f sec' % (dt-self.frame_dt)
                
                row_start = time.time()
                
            count += 1
    
    def draw_frame(self, frame):
        for i, w in enumerate(self.writers):
            try:
                w.send_frame(frame)
            except IOError:
                w.exit()
                del self.writers[i]
                    
class PatternWriter(threading.Thread):
    
    def __init__(self, framerate):
        super(PatternWriter, self).__init__()
        self.daemon = True
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
            #if r.has_key('status') and r['status'] == 'exiting':
            #    raise SystemExit
            
        self.pipe_out.send(pattern_data)
    
    def run(self):
        self.open_port()
        try:
            while True:
                frame = self.pipe_in.recv()
                
                if len(frame) == 0:
                    raise SystemExit
                
                self.draw_frame(frame)
        
        except (KeyboardInterrupt, SystemExit):
            self.exit()
            return
    
    def exit(self):
        try:
            while self.pipe_in.poll():  # Empty buffers
                self.pipe_in.recv()
            self.pipe_in.send(dict(status='exiting'))
            self.pipe_in.close()
        except Exception, e:
            pass
        self.close_port()
        print 'Writer exit'


class WebsocketWriter(PatternWriter):
    
    def __init__(self, framerate, websocket):
        super(WebsocketWriter, self).__init__(framerate)
        self.websocket = websocket

    def open_port(self):
        pass
        
    def draw_frame(self, frame):
        # print "Drawing frame:", [chr(x) for x in frame]
        json_frame = ['{"status":"ok", "frame" : [']
        
        for i in range(0, len(frame)-3, 3):
            r, g, b = frame[i:i+3]
            json_frame.extend(['"rgb(',str(r),',',str(g),',',str(b),')",'])
        
        r, g, b = frame[-3:]
        json_frame.extend(['"rgb(',str(r),',',str(g),',',str(b),')"]}'])
        json_data = ''.join(json_frame)
        
        self.client_push(json_data)
        
    def client_push(self, data):
        #print 'writing data'
        try:
            self.websocket.send(str(data))
        except IOError:
            print "Websocket closed"
            raise
                
    def close_port(self):
        self.client_push('{"status":"exiting"}')
        time.sleep(1.0)
        self.websocket.close()
        
