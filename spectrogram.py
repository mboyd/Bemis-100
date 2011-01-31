from __future__ import division

""" Record a few seconds of audio and save to a WAVE file. """

import pyaudio
import wave
import sys
import matplotlib.pyplot as plt
import numpy as np
import sys, os, pygame
from pygame.locals import *
from threading import Thread
from pattern import output_char

chunk = 2048
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
		      input = True, frames_per_buffer = chunk)
        while True:
            self.data = stream.read(chunk)

# def samples_to_rgb(block):
#     return fft_to_rgb(np.fft.rfft(block),len(block))

def rfft_to_rgb(c,c_prev, block_size = 2048, sample_rate = RATE):
    '''Converts a list of rFFT components to an R G B triple'''
    out = np.zeros(3,dtype=np.uint8)
#     freq_cutoffs = np.array([[5000,20000],[500,5000],[0,500]]) # R,G,B (Hz)
    freq_cutoffs = np.array([[200000,200000],[200000,200000],[0,150]]) # R,G,B (Hz)
    for i in range(len(freq_cutoffs)):
        fft_cutoffs = freq_cutoffs[i] * block_size/sample_rate
        if fft_cutoffs[0] >= len(c):
            out[i] = 0
        else:
            x = int(0.000255 *\
                    (sum([abs(j) for j in c[1:fft_cutoffs[1]]])-\
                sum([abs(j) for j in c_prev[1:fft_cutoffs[1]]])))
            if x < 7:
                out[i] = 0
            else:
                out[i] = output_char(np.log(x) * 100)
    return out

class SpectrogramPattern:
    def __init__(self, num_boards = 83):
        self.listener = Listener()
        self.listener.start()
        self.chunk = 2048
        target_width = num_boards * 6
        self.row = np.zeros(target_width,dtype=np.uint8)
        self.c = np.fft.rfft([ord(i) for i in self.listener.data])

    def get_line(self):
        c_prev = self.c
        self.c = np.fft.rfft([ord(i) for i in self.listener.data])
#         self.row=np.tile(rfft_to_rgb(self.c,c_prev),len(self.row)//3)
        self.row = np.roll(self.row,3)
        self.row.put([0,1,2],rfft_to_rgb(self.c,c_prev))
        return bytearray(self.row)

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


