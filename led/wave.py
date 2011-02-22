from __future__ import division

from multiprocessing import Process, Pipe
import pattern
import numpy as np

T = 1; # "Tension" 
mu = 1; # "mass per length"
friction = 0; # frictional force per velocity
dt = .5;

class WavePattern:
    def __init__(self,num_boards = 83):
        self.pixels = num_boards*2
        self.pos = np.zeros(self.pixels)
        self.vel = np.zeros(self.pixels)
        self.acc = np.zeros(self.pixels)
        self.out = np.zeros(self.pixels*3)

    def get_line(self):
        # for i in range(1,self.pixels-2):
            # self.acc[i] = ((self.pos[i+1]-2*self.pos[i]+\
                    # self.pos[i-1])*T-friction*self.vel[i])/mu;

        # for i in range(1,self.pixels-2):
            # self.vel[i] = (self.vel[i] + self.acc[i]*dt);

        # for i in range(1,self.pixels-2):
            # self.pos[i] = self.pos[i] + self.vel[i]*dt;

        self.acc[1:self.pixels-1] = ((self.pos[2:self.pixels]-\
                2*self.pos[1:self.pixels-1]+\
                self.pos[0:self.pixels-2])*T-friction*self.vel[1:self.pixels-1])/mu
        
        self.vel[1:self.pixels-1] += self.acc[1:self.pixels-1]*dt

        self.pos[1:self.pixels-1] += self.vel[1:self.pixels-1]*dt

        for i in range(self.pixels):
            # new_point = abs(self.data[i])
            self.new_point = self.pos[i]
            if self.new_point > 1:
                self.new_point = 1
            elif self.new_point < -1:
                self.new_point = -1
            if self.new_point > 0:
                # self.new_data = np.array([0,0,self.new_point*255])
                # self.new_data = [0,0,self.new_point*255]
                self.out[i*3] = 0
                self.out[i*3+1] = 0
                self.out[i*3+2] = self.new_point*255
            elif self.new_point < 0:
                # self.new_data = np.array([-self.new_point*255,0,0])
                # self.new_data = [-self.new_point*255,0,0]
                self.out[i*3] = -self.new_point*255
                self.out[i*3+1] = 0
                self.out[i*3+2] = 0
            else:
                # self.new_data = np.zeros(3)
                # self.new_data = [0,0,0]
                self.out[i*3] = 0
                self.out[i*3+1] = 0
                self.out[i*3+2] = 0
            # self.out[i*3:i*3+3] = self.new_data
        return bytearray((pattern.encode_char(c) for c in self.out))

    def __iter__(self):
        # start_data = np.array(\
                # [0]+\
                # [0]*np.floor(self.pixels/2-31)+\
                # [1]*60+\
                # [0]*np.ceil(self.pixels/2-31)+\
                # [0])
        start_data = np.array(\
                [0]+\
                [1]*20+\
                [0]*int(self.pixels-22)+\
                [0])

        # start_data = np.zeros(self.num_boards*2)
        # for i in range(len(start_data)):
            # start_data[i] = np.sin(i*np.pi*2/(self.num_boards*2-1))

        self.pos += start_data
        return iter(self.get_line,None)

    
    
