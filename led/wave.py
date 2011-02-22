from __future__ import division

from multiprocessing import Process, Pipe
import pattern
import numpy as np

T = .1; # "Tension" 
mu = 1; # "mass per length"
friction = 0; # frictional force per velocity
dt = .1;

class WavePattern:
    def __init__(self,num_boards = 83):
        self.pixels = num_boards*2
        self.pos = np.zeros(self.pixels)
        self.vel = np.zeros(self.pixels)
        self.acc = np.zeros(self.pixels)

    def get_line(self):
        self.pos[0] = 0
        self.pos[len(self.pos)-1] = 0
        
        for i in range(1,self.pixels-2):
            self.acc[i] = ((self.pos[i+1]-2*self.pos[i]+\
                    self.pos[i-1])*T-friction*self.vel[i])/mu;

        for i in range(1,self.pixels-2):
            self.vel[i] = (self.vel[i] + self.acc[i]*dt);

        for i in range(1,self.pixels-2):
            self.pos[i] = self.pos[i] + self.vel[i]*dt;

        out = np.zeros((self.pixels,3))
        for i in range(len(out)):
            # new_point = abs(self.data[i])
            new_point = self.pos[i]
            if new_point > 1:
                new_point = 1
            if new_point < -1:
                new_point = -1
            if new_point > 0:
                out[i] = [0,0,new_point*255]
            if new_point < 0:
                out[i] = [-new_point*255,0,0]
        out = np.reshape(out,(-1))
        return bytearray([pattern.encode_char(c) for c in out])

    def __iter__(self):
        start_data = np.array(\
                [0]+\
                [0]*np.floor(self.pixels/2-11)+\
                [1]*20+\
                [0]*np.ceil(self.pixels/2-11)+\
                [0])

        # start_data = np.zeros(self.num_boards*2)
        # for i in range(len(start_data)):
            # start_data[i] = np.sin(i*np.pi*2/(self.num_boards*2-1))

        self.pos += start_data
        return iter(self.get_line,None)

    
    
