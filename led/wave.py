from __future__ import division

from multiprocessing import Process, Pipe
import pattern
import numpy as np
import random

T = .5; # "Tension" 
mu = 1; # "mass per length"
friction = 0; # frictional force per velocity
dt = .5;

class WavePattern:
    def __init__(self,num_boards = 83):
        self.pixels = num_boards*2
        print self.pixels, "pixels in use"
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

        self.vel[1:self.pixels-1] *= .95

        self.pos[1:self.pixels-1] += self.vel[1:self.pixels-1]*dt

        if random.random() < .02:
            pulse_center = random.randrange(0, self.pixels)
            pulse_width = random.randrange(1, 15)
            if random.random() < .5:
                pulse_sign = -1
            else:
                pulse_sign = 1
            self.pos[max(1, pulse_center - pulse_width//2):min(self.pixels-1, 
                                                               pulse_center + pulse_width//2)] = pulse_sign

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
                self.out[i*3+2] = int(self.new_point*255)
            elif self.new_point < 0:
                # self.new_data = np.array([-self.new_point*255,0,0])
                # self.new_data = [-self.new_point*255,0,0]
                self.out[i*3] = int(-self.new_point*255)
                self.out[i*3+1] = 0
                self.out[i*3+2] = 0
            else:
                # self.new_data = np.zeros(3)
                # self.new_data = [0,0,0]
                self.out[i*3] = 0
                self.out[i*3+1] = 0
                self.out[i*3+2] = 0
            # self.out[i*3:i*3+3] = self.new_data
        return bytearray((int(i) for i in self.out))

    def __iter__(self):
        pulse_width = 20
        start_data = np.array(\
                [0]+\
                [0]*np.floor(self.pixels/2-(pulse_width//2+1))+\
                [1]*pulse_width+\
                [0]*np.ceil(self.pixels/2-(pulse_width//2+1))+\
                [0])
        print "start data", start_data
        # start_data = np.array(\
                # [0]+\
                # [1]*20+\
                # [0]*int(self.pixels-22)+\
                # [0])

        # start_data = np.zeros(self.num_boards*2)
        # for i in range(len(start_data)):
            # start_data[i] = np.sin(i*np.pi*2/(self.num_boards*2-1))

        self.pos += start_data
        return iter(self.get_line,None)

    
    
