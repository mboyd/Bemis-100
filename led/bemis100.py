#!/usr/bin/env python2.6
from __future__ import division

import ledctl, pattern
import serial, threading

class Bemis100(ledctl.LEDController):
    def __init__(self, device, framerate=30, num_boards=83, start_websocket=True):
        super(Bemis100, self).__init__(device, framerate=framerate)
        
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
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                timeout=0.5,
                writeTimeout=0)
        self.blank()

    def close_port(self):
        self.blank()
        self.port.close()

    def draw_frame(self, frame):
        self.port.write('B')
        self.port.write(bytearray([encode_char(c) for c in frame]))
 
    def blank(self):
        '''Turn off all the LEDs. We do this before startup to make sure the
        power supplies are not loaded by the LEDs when they come online.'''
        f = bytearray("\x00\x00\x00"*self.num_boards*2)
        self.draw_frame(f)

#
# PWM Routines
#

PWM_BITS = 8
PWM_BINS = PWM_BITS + 1
PWM_CUTOFFS = [int(255.*i/(PWM_BINS)) for i in range(1, PWM_BINS+1)]
PWM_VALS = [2**i-1 for i in range(PWM_BINS)]

PWM_CUTOFFS = [0] + [5.33*i+3 for i in range(48)] + [255]

def encode_char(value):
    if (value < 6):
        return 0
    else:
        return max(int(PWM_LOOKUP[value]), 9)

def _encode_char(value):
    """Return a bitmask for a pwm representation of the 8-bit
    integer value. Our firmware only implements 8 shades, so we indicate the
    brightness of a pixel by the number of 1s in an 8-bit string, which we
    transmit as a single character."""
    
    for i in range(len(PWM_CUTOFFS)):
        if value <= PWM_CUTOFFS[i]:
            return PWM_CUTOFFS[i]
            #return PWM_VALS[i]
    raise ValueError, "Pixel value %i out of range" % value

PWM_LOOKUP = [_encode_char(i) for i in range(256)]

def decode_char(x):
    '''Undo the conversion from char values to bytes, in which the value is
    indicated by the number of 1s in the byte'''
    return x

PWM_DECODE_LOOKUP = {PWM_VALS[0] : 0}
for i in range(1, PWM_BINS-1):
    PWM_DECODE_LOOKUP[PWM_VALS[i]] = int(round((PWM_CUTOFFS[i] - PWM_CUTOFFS[i-1]) / 2 + PWM_CUTOFFS[i-1]))
PWM_DECODE_LOOKUP[PWM_VALS[-1]] = 255
