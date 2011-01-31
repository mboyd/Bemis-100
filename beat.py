from __future__ import division

""" Record a few seconds of audio and save to a WAVE file. """

import pyaudio
import wave
import sys
import numpy as np
import sys, os, pygame
from pygame.locals import *
from threading import Thread
import Image as im

chunk = 2048
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 44100

def output_char(value):
    """Return a sequence of boolean states for a pwm representation of the 8-bit
    integer value. Our firmware only implements 8 shades, so we indicate the
    brightness of a pixel by the number of 1s in an 8-bit string, which we
    transmit as a single character."""
    
    # FIXME: Really? Awwww. 
    
    raw = str(int(value>=255*1))+\
            str(int(value>=255*7/8))+\
            str(int(value>=255*6/8))+\
            str(int(value>=255*5/8))+\
            str(int(value>=255*4/8))+\
            str(int(value>=255*3/8))+\
            str(int(value>=255*2/8))+\
            str(int(value>=255*1/8))
    return int(raw,2)

image = im.open('rainbow166x1.gif')
image = image.convert('RGB')
image_data = []
(width,height) = image.size
frame = image.getdata()
row_pix = (frame[i] for i in range(width))
row_raw = (b for pix in row_pix for b in pix)
row = bytearray((output_char(c) for c in row_raw))
    
image_data.append(row)
                

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


def rfft_to_val(c,block_size=2048,sample_rate = RATE):
    freq_cutoffs = np.array([0,150])
    fft_cutoffs = freq_cutoffs * block_size/sample_rate
    x = sum([abs(j) for j in c[1:fft_cutoffs[1]]])
    if x <= 0:
        x = 0
    val = x
    if val < 0:
        val = 0
    return int(val*255/100000)


class BeatPattern:
    def __init__(self, num_boards = 83):
        self.listener = Listener()
        self.listener.start()
        self.chunk = 2048
        target_width = num_boards * 6
        self.row = np.zeros(target_width,dtype=np.uint8)
        self.c = np.fft.rfft([ord(i) for i in self.listener.data])

    def get_line(self):
        self.c = np.fft.rfft([ord(i) for i in self.listener.data])
#         self.row=np.tile(rfft_to_rgb(self.c,c_prev),len(self.row)//3)
        val = rfft_to_val(self.c)
        return row[0:val] + bytearray([0 for i in range(len(self.row)-val)])


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


