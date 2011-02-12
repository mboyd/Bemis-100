from __future__ import division

""" Record a few seconds of audio and save to a WAVE file. """

import pyaudio
import wave
import sys
import numpy as np
import sys, os
from threading import Thread
import pattern

CHUNK = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 44100
BAR_PATTERN = [255,0,0]
FREQ_RANGE = [0,200] #Hz
GAIN = 0.0017

                

class Listener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon=True
        self.data = [chr(int(i)) for i in np.zeros(chunk)]

    def run(self):
        p = pyaudio.PyAudio()
        stream = p.open(input_device_index = 3, format = FORMAT, channels = CHANNELS,
                        rate = RATE, input = True, frames_per_buffer = chunk)
        while True:
            try:
                self.data = stream.read(chunk)
            except:
                break


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
    return np.fft.rfft([ord(i) for i in data])


class BeatPattern:
    '''Does an overlay on top of the base pattern which does fancy audio
    tracking things.'''
    def __init__(self, base_pattern):
        self.base_pattern = base_pattern.__iter__()
        self.start_listener()

    def start_listener(self):
        self.listener = Listener()
        self.listener.start()
        self.chunk = CHUNK
        self.last_out = np.zeros(len(self.image_data[self.pattern_index]))
        self.old_vals = [0 for i in range(8)]
        self.c = data_to_rfft(self.listener.data)

    def get_line(self):
        if not self.listener.isAlive():
            self.listener = Listener()
            self.listener.start()
        self.row = np.array([i for i in self.base_pattern.next()])
        self.out = np.array([0 for i in range(target_width)])

        self.update_val()

        self.mask_row()

        self.add_bar()

        averaged_out = self.out*0.75+self.last_out*0.25
        self.last_out = out
        return bytearray([encode_char(c) for c in averaged_out]) 

    def update_val(self):
        c = data_to_rfft(self.listener.data)
        self.val = rfft_to_val(c,freq_range=FREQ_RANGE,gain=GAIN)
        self.val = min(self.val,target_width/2-9)
        self.old_vals.insert(0,self.val)
        self.old_vals.pop()

    def mask_row(self):
        target_width=len(self.row)
        pattern_start = int(int(target_width/2)-self.val)
        pattern_stop = int(int(target_width/2)+self.val)
        self.out[pattern_start:pattern_stop] = \
                self.row[pattern_start:pattern_stop]

    def add_bar(self):
        max_old_val = max(self.old_vals)
        bar_width = len(BAR_PATTERN)
        bar_low = int(target_width/2-max_old_val) - bar_width
        bar_low = bar_low - bar_low % bar_width
        bar_high = int(target_width/2+max_old_val) + bar_width
        bar_high = bar_high + bar_width - bar_high % bar_width
        self.out[bar_low:bar_low+bar_width] = BAR_PATTERN
        self.out[bar_high-bar_width:bar_high] = BAR_PATTERN 


    def __iter__(self):
        return iter(self.get_line,None)


# def readWave(fn):
#     wf = wave.open(fn, 'rb')
#     data = wf.readframes(chunk)
#     all = ''
#     while data != '':
#         all+=data
#         data = wf.readframes(chunk)
#     return [ord(char) for char in all]

# def recordAudio(seconds):
#     p = pyaudio.PyAudio()
#     stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,
#               input = True, frames_per_buffer = chunk)
#     all = np.zeros(int(RATE*seconds),dtype=np.int8)
#     print "recording"
#     for i in range(int(RATE/chunk*seconds)):
#         data = stream.read(chunk)
#         all[i*chunk:(i+1)*chunk] = [ord(char) for char in data]
#     print "done"

#     stream.close()
#     p.terminate()
#     return all

# def record_samples(samples,chunk=1024):
#     p = pyaudio.PyAudio()
#     stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,
#               input = True, frames_per_buffer = chunk)
#     all = np.zeros(samples,dtype=np.int8)
#     print "recording"
#     for i in range(samples//chunk):
#         data = stream.read(chunk)
#         all[i*chunk:(i+1)*chunk] = [ord(char) for char in data]
#     print "done"

#     stream.close()
#     p.terminate()
#     return all


# def plotBeats(all):
#     fft_block_size = 1024
#     fft_low = []
#     cutoff_freq = 400 # Hz
#     fft_cutoff = cutoff_freq * fft_block_size / RATE
#     for i in range(len(all)//fft_block_size):
#         fft_low.append(sum(abs(np.fft.rfft(all[i*fft_block_size:(i+1)*fft_block_size])[:fft_cutoff])))
#     plt.figure()
#     plt.plot(np.diff(fft_low))

# def plotSpectrogram(all):
#     plt.figure()
#     plt.specgram(all, Fs=44100)

# color-> frequency
# position -> time in the past

# listen to the audio, decode with FFT. 
# break up fft into three bands (red -> high, blue -> low freq)
# sum over the components in each band is the brightness of that color at the
# head
# pattern propagates from head to tail

# how do we scale the fft values to get an actual brightness?
# probably just trial and error

# i just need to create an array of rgb triplets. so, let's load in the 


