from __future__ import division

""" Record a few seconds of audio and save to a WAVE file. """

import pyaudio
# import wave
# import matplotlib.pyplot as plt
import numpy as np
import sys, os, pygame
from pygame.locals import *
from threading import Thread
from pattern import output_char
from beat import data_to_rfft
from beat import rfft_to_val

chunk = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 44100

class Listener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon=True
        self.data = [chr(int(i)) for i in np.zeros(chunk)]

    def run(self):
        p = pyaudio.PyAudio()
        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,
		      input = True, frames_per_buffer = chunk, input_device_index=3)
        while True:
            self.data = stream.read(chunk)

# def samples_to_rgb(block):
#     return fft_to_rgb(np.fft.rfft(block),len(block))


def rfft_to_rgb(c,last_val, block_size = 2048, sample_rate = RATE):
    '''Converts a list of rFFT components to an R G B triple'''
    out = np.zeros(3,dtype=np.uint8)
#     freq_cutoffs = np.array([[5000,20000],[500,5000],[0,500]]) # R,G,B (Hz)
    freq_cutoffs = np.array([[200000,200000],[200000,200000],[0,100]]) # R,G,B (Hz)
    for i in range(len(freq_cutoffs)):
        fft_cutoffs = freq_cutoffs[i] * block_size/sample_rate
        if fft_cutoffs[0] >= len(c):
            out[i] = 0
        else:
            x = int(0.000255 *\
                    (sum([abs(j) for j in\
                          c[fft_cutoffs[0]:fft_cutoffs[1]]])-last_val))
            print x
            if x < 20:
                out[i] = 0
            else:
                out[i] = output_char(np.log(x) * 100)
    return out



class SpectrogramPattern:
    def __init__(self, num_boards = 83):
        self.listener = Listener()
        self.listener.start()
        self.chunk = 1024
        target_width = num_boards * 6
        self.row = np.zeros(target_width,dtype=np.uint8)
		#       self.out = rfft_to_rgb(data_to_rfft(self.listener.data),0)

    def get_line(self):
        #       last_val = self.out[2]
        #       self.out = rfft_to_rgb(data_to_rfft(self.listener.data),last_val)
        data = self.listener.data
        #       red_val = rfft_to_val(data_to_rfft(data),
        #                             freq_range=[5000,10000],gain=255/2000000)
        red_val = 0
        #       blue_val = rfft_to_val(data_to_rfft(data),
        #                              freq_range=[0,100],gain=255/35000)
        blue_val = rfft_to_val(data_to_rfft(data),
                               freq_range=[0,10000],gain=255/1000000)
        self.row = np.roll(self.row,3)
        self.row.put([0,1,2],[output_char(red_val),0,output_char(blue_val)])
        return bytearray(self.row)

    def __iter__(self):
        return iter(self.get_line,None)



