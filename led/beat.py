from __future__ import division

""" Record a few seconds of audio and save to a WAVE file. """

import pyaudio
import wave
import sys
import numpy as np
import sys, os
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_byte, c_double
import pattern

CHUNK = 512
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 44100
BAR_PATTERN = [255,0,0]
FREQ_RANGE = [0,200] #Hz
GAIN = 0.0017
RMS_GAIN = 50000
RMS_CHUNK = 512               

def listen(chunk,data):
    p = pyaudio.PyAudio()
    stream = p.open(input_device_index = 3, format = FORMAT, channels = CHANNELS,
                    rate = RATE, input = True, frames_per_buffer = chunk)
    while True:
        try:
            new_data = stream.read(chunk)
            for i in range(len(new_data)):
                data[i] = c_byte(ord(new_data[i]))
        except:
            pass

def rfft_to_val(c,freq_range = [0,10000],gain = 255/750000,
                block_size=1024,sample_rate = RATE):
    freq_cutoffs = np.array(freq_range)
    fft_cutoffs = freq_cutoffs * block_size/sample_rate
    x = sum([abs(j) for j in c[1:fft_cutoffs[1]]])
    if x <= 0:
        x = 0
    val = x
    if val < 0:
        val = 0
    return int(val*gain)

def data_to_rfft(data):
    return np.fft.rfft([i for i in data])


class BeatPattern:
    '''Does an overlay on top of the base pattern which does fancy audio
    tracking things.'''
    def __init__(self, base_pattern, freq_range=FREQ_RANGE,gain=GAIN,
            chunk = CHUNK):
        self.base_pattern = base_pattern
        self.base_pattern_iter = base_pattern.__iter__()
        self.chunk = chunk

    def start_listener(self):
        lock = Lock()
        # print [ord(i) for i in start_string]
        self.data = Array(c_byte,[0]*self.chunk,lock=lock)
        # print [ord(i) for i in self.data.value]
        proc = Process(target = listen, args=(self.chunk, self.data))
        proc.daemonic = True
        proc.start()
        # self.listener = Listener(self.chunk)
        # self.listener.start()
        try:
            self.last_out = np.zeros(len(self.base_pattern_iter.next()))
        except StopIteration:
            self.base_pattern_iter = self.base_pattern.__iter__()
            self.last_out = np.zeros(len(self.base_pattern_iter.next()))
        self.old_vals = [0 for i in range(8)]
        self.c = data_to_rfft(self.data)

    def get_line(self):
        # if not self.listener.isAlive():
            # print "listener died"
            # self.listener = Listener(self.chunk)
            # self.listener.start()
        try:
            self.row = np.array([i for i in self.base_pattern_iter.next()])
        except StopIteration:
            self.base_pattern_iter = self.base_pattern.__iter__()
            self.row = np.array([i for i in self.base_pattern_iter.next()])
        self.out = np.zeros(len(self.row))
        self.target_width = len(self.row)

        self.update_val()

        self.mask_row()

        self.add_bar()

        averaged_out = self.out*0.75+self.last_out*0.25
        self.last_out = self.out
        return bytearray([pattern.encode_char(c) for c in averaged_out]) 

    def update_val(self):
        # print '\n\n'
        # print [ord(i) for i in self.data.value]
        # print '\n\n'
        # c = data_to_rfft(self.listener.data)
        c = data_to_rfft(self.data)
        self.val = rfft_to_val(c,freq_range=FREQ_RANGE,gain=GAIN)
        self.val = min(self.val,self.target_width/2-9)
        self.old_vals.insert(0,self.val)
        self.old_vals.pop()

    def mask_row(self):
        pattern_start = int(int(self.target_width/2)-self.val)
        pattern_stop = int(int(self.target_width/2)+self.val)
        self.out[pattern_start:pattern_stop] = \
                self.row[pattern_start:pattern_stop]

    def add_bar(self):
        max_old_val = max(self.old_vals)
        bar_width = len(BAR_PATTERN)
        bar_low = int(self.target_width/2-max_old_val) - bar_width
        bar_low = bar_low - bar_low % bar_width
        bar_high = int(self.target_width/2+max_old_val) + bar_width
        bar_high = bar_high + bar_width - bar_high % bar_width
        self.out[bar_low:bar_low+bar_width] = BAR_PATTERN
        self.out[bar_high-bar_width:bar_high] = BAR_PATTERN 


    def __iter__(self):
        self.start_listener()
        return iter(self.get_line,None)

class BeatPatternRMS(BeatPattern):
    '''Same as the beat pattern, but uses the RMS as a measure of amplitude,
    rather than doing any FFTs'''
    def __init__(self, base_pattern, gain=RMS_GAIN,chunk = RMS_CHUNK):
        self.base_pattern = base_pattern
        self.base_pattern_iter = base_pattern.__iter__()
        self.chunk = chunk
        self.start_listener()

    def update_val(self):
        data = np.array([ord(i) for i in self.listener.data])
        # print min(data-127), np.mean(data-127), max(data-127)
        # self.val = np.sqrt(np.mean((data)**2))
        self.val = np.sqrt(np.mean((data-np.mean(data))**2))
        self.val = min(self.val,self.target_width/2-9)
        self.old_vals.insert(0,self.val)
        self.old_vals.pop()
        
        


