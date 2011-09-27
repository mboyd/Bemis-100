from __future__ import division

import ledctl, pattern
import serial
import time

class GEController(ledctl.LEDController):
    def __init__(self, device, framerate=20, num_boards=50, start_websocket=False):
        super(GEController, self).__init__(device, framerate=framerate, 
                                    start_websocket=start_websocket)
        
        self.num_boards = num_boards
        if not device == 'sim':
            self.add_writer(GEWriter(device, num_boards, framerate))

class GEWriter(ledctl.PatternWriter):
    
    def __init__(self, device, num_boards, framerate):
        super(GEWriter, self).__init__(framerate)
        
        self.device = device
        self.port = None
        self.num_boards = num_boards
    
    def open_port(self):
        self.port = serial.Serial(port=self.device,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                timeout=0.5,
                writeTimeout=0)
        self.blank()

    def close_port(self):
        self.blank();
        self.port.close()

    def draw_frame(self, frame):
        self.port.write('B')
        for i in range(len(frame)):
            self.port.write(frame[3*i:3*i + 3])
            time.sleep(.001) #give the controller enough time to write the new data
 
    def blank(self):
        '''Turn off all the LEDs. We do this before startup to make sure the
        power supplies are not loaded by the LEDs when they come online.'''
        f = bytearray("\x00\x00\x00"*self.num_boards)
        self.draw_frame(f)
    def wait_for_finish(self):
        while True:
            pass