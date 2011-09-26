#!/usr/bin/env python2.6
from __future__ import division

import ledctl, pattern
import serial

class Bemis100(ledctl.LEDController):
    def __init__(self, device, framerate=30, num_boards=83, start_websocket=True):
        super(Bemis100, self).__init__(device, framerate=framerate, 
                                    start_websocket=start_websocket)
        
        self.num_boards = num_boards
        if not device == 'sim':
            self.add_writer(Bemis100Writer(device, num_boards, framerate))

class Bemis100Writer(ledctl.PatternWriter):
    
    def __init__(self, device, num_boards, framerate):
        super(Bemis100Writer, self).__init__(framerate)
        
        self.device = device
        self.port = None
        self.num_boards = num_boards
    
    def open_port(self):
        self.port = serial.Serial(port=self.device,
                # baudrate=230400,
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
        self.port.write(frame)
 
    def blank(self):
        '''Turn off all the LEDs. We do this before startup to make sure the
        power supplies are not loaded by the LEDs when they come online.'''
        f = bytearray("\x00\x00\x00"*self.num_boards*2)
        self.draw_frame(f)
