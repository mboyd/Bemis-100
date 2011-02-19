from __future__ import division

from beat import listen, data_to_rfft
from multiprocessing import Process, Lock, Pipe

import pattern
import numpy as np

GRADIENT_LEVELS = 100
FREQ_RANGE = [0,2500]
GAIN = 0.00225
CHUNK = 512
RATE = 44100
DEFAULT_NUM_BOARDS = 83

# The gradient is intended to be a 1-D bytearray of values in RGB order. Low
# amplitudes will correspond to the RGB values in the beginning of the byte
# array, and high amplitudes to the values at the end. 
gradient = pattern.Bemis100Pattern('../Patterns/rainbow166x1.gif', 
        GRADIENT_LEVELS/2).__iter__().next()


# Record audio chunk -> fft -> list same length as chunk
# normalize by gain -> list same length as chunk
# load gradient pattern -> list of length GRADIENT_LEVELS * 3
# map pixels in self.out to normalized coefficients
# step through self.out (length num_boards*6)
# each RGB block equals the values from gradient indexed by the normalized coeff
# corresponding to that pixel
# 

class GraphEqPattern:
    def __init__(self, gradient = gradient, num_boards = DEFAULT_NUM_BOARDS,
           freq_range = FREQ_RANGE, gain = GAIN, chunk = CHUNK):
       self.gradient = np.reshape(np.array([i for i in gradient]),(-1,3))
       self.chunk = chunk
       self.gain = gain
       self.out = np.zeros((num_boards*2,3))
       num_bars = (freq_range[1]-freq_range[0])*chunk / RATE
       self.bar_width = num_boards*2//num_bars # width of each freq. bar in px

    def start_listener(self):
        self.parent_conn, child_conn = Pipe(duplex=False)
        proc = Process(target = listen, args=(self.chunk,child_conn))
        proc.start()
        self.data = self.parent_conn.recv()

    def get_coeffs(self):
        while self.parent_conn.poll():
            self.data = self.parent_conn.recv()
        c = data_to_rfft(self.data)
        self.normalized = [int(abs(i)*self.gain) for i in c]
        # print self.normalized

    def colorize(self):
        for i in range(len(self.out)):
            ndx = self.normalized[int(i//(self.bar_width))]
            if ndx >= len(self.gradient):
                ndx = len(self.gradient)-1
            # print "i", i, "out",len(self.out),'ndx',ndx,'grad',len(self.gradient)
            self.out[i] = self.gradient[ndx]

    def get_line(self):
        self.get_coeffs()
        self.colorize()
        line = np.reshape(self.out,(-1))
        return bytearray([pattern.encode_char(int(c)) for c in line])

    def __iter__(self):
        self.start_listener()
        return iter(self.get_line,None)


    
