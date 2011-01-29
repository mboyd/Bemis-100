from __future__ import division

""" Record a few seconds of audio and save to a WAVE file. """

import pyaudio
import wave
import sys
import matplotlib.pyplot as plt
import numpy as np
import sys, os, pygame
from pygame.locals import *

chunk = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 44100

def readWave(fn):
    wf = wave.open(fn, 'rb')
    data = wf.readframes(chunk)
    all = ''
    while data != '':
        all+=data
        data = wf.readframes(chunk)
    return [ord(char) for char in all]

def recordAudio(seconds):
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,
		      input = True, frames_per_buffer = chunk)
    all = np.zeros(int(RATE*seconds),dtype=np.int8)
    print "recording"
    for i in range(int(RATE/chunk*seconds)):
        data = stream.read(chunk)
        all[i*chunk:(i+1)*chunk] = [ord(char) for char in data]
    print "done"

    stream.close()
    p.terminate()
    return all

def record_samples(samples,chunk=1024):
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,
		      input = True, frames_per_buffer = chunk)
    all = np.zeros(samples,dtype=np.int8)
    print "recording"
    for i in range(samples//chunk):
        data = stream.read(chunk)
        all[i*chunk:(i+1)*chunk] = [ord(char) for char in data]
    print "done"

    stream.close()
    p.terminate()
    return all


def plotBeats(all):
    fft_block_size = 1024
    fft_low = []
    cutoff_freq = 400 # Hz
    fft_cutoff = cutoff_freq * fft_block_size / RATE
    for i in range(len(all)//fft_block_size):
        fft_low.append(sum(abs(np.fft.rfft(all[i*fft_block_size:(i+1)*fft_block_size])[:fft_cutoff])))
    plt.figure()
    plt.plot(np.diff(fft_low))

def plotSpectrogram(all):
    plt.figure()
    plt.specgram(all, Fs=44100)

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

timeOffset = 0
newPoint = [0, 0, 0]

def samples_to_rgb(block):
    block = [ord(char) for char in block]
    return fft_to_rgb(np.fft.rfft(block),len(block))

def fft_to_rgb(c, block_size = 1024, sample_rate = RATE):
    '''Converts a list of rFFT components to an R G B triple'''
    plt.plot(c)
    plt.show()
    out = np.zeros(3,dtype=np.uint8)
    freq_cutoffs = np.array([[5000,20000],[500,5000],[0,500]]) # R,G,B (Hz)
    for i in range(len(freq_cutoffs)):
        fft_cuttoffs = freq_cutoffs[i] * block_size/sample_rate
        out[i] = int(0.0000255 * sum([abs(j) for j in\
            c[fft_cuttoffs[0]:fft_cuttoffs[1]]]))
    return out

class SpectrogramPattern:
    def __init__(self, num_boards = 83):
        self.p = pyaudio.PyAudio()
        self.chunk = 1024
        target_width = num_boards * 6
        self.row = np.zeros(target_width,dtype=np.uint8)

    def get_line(self):
        self.stream = self.p.open(format = FORMAT, channels = CHANNELS, 
                rate = RATE, input = True, frames_per_buffer = chunk)
        new_data = self.stream.read(self.chunk)
        self.row = np.roll(self.row,3)
        self.row.put([0,1,2],samples_to_rgb(new_data))
#         print self.row
        self.stream.close()
        return bytearray(self.row)

        
    def __iter__(self):
        return iter(self.get_line,None)




