from __future__ import division

from beat import listen, data_to_rfft
from multiprocessing import Process, Lock, Pipe

import pattern

GRADIENT_LEVELS = 100
FREQ_RANGE = [0,10000]
GAIN = 1
CHUNK = 512
RATE = 44100
DEFAULT_NUM_BOARDS = 83

# The gradient is intended to be a 1-D bytearray of values in RGB order. Low
# amplitudes will correspond to the RGB values in the beginning of the byte
# array, and high amplitudes to the values at the end. 
gradient = pattern.Bemis100Pattern('../Patterns/rainbow166x1.gif', 
        GRADIENT_LEVELS/2).__iter__().next()

class GraphEqPattern:
    def __init__(self, gradient = gradient, num_boards = DEFAULT_NUM_BOARDS,
           freq_range = FREQ_RANGE, gain = GAIN, chunk = CHUNK):
       self.gradient = gradient
       self.chunk = chunk
       self.gain = gain
       self.out = np.zeros(num_boards*6)
       num_bars = (freq_range[1]-freq_range[0])*chunk / RATE
       self.bar_width = num_boards*2//num_bars # width of each freq. bar in px

    def start_listener(self):
        self.parent_conn, child_conn = Pipe(duplex=False)
        proc = Process(target = listen, args=(self.chunk,child_conn))
        proc.start()
        self.get_coeffs()

    def get_coeffs(self):
        while self.parent_conn.poll():
            self.data = self.parent_conn.recv()
        c = data_to_rfft(self.data)
        self.normalized = c*self.gain

    def colorize(self):
        for i in range(len(self.out)//3):
            ndx = self.normalized[i//(self.bar_width*3)]
            if ndx > len(self.gradient)//3:
                ndx = len(self.gradient)//3
            self.out[i:i+3] = self.gradient[i:i+3]
            self.out[i] = self.normalized[i//self.bar_width]

    def get_line(self):


    
