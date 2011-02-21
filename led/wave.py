from __future__ import division

from multiprocessing import Process, Pipe
import pattern
import numpy as np

def make_wave(pixels,input_parent,data_child):
    pos = np.zeros(pixels)
    vel = np.zeros(pixels)
    acc = np.zeros(pixels)
    T = .1; # "Tension" 
    mu = 1; # "mass per length"
    friction = 0; # frictional force per velocity
    dt = .1;
    while True:
        while input_parent.poll():
            pos += input_parent.recv()
        pos[0] = 0
        pos[len(pos)-1] = 0
        for i in range(1,pixels-2):
            acc[i] = ((pos[i+1]-2*pos[i]+pos[i-1])*T-friction*vel[i])/mu;

        for i in range(1,pixels-2):
            vel[i] = (vel[i] + acc[i]*dt);

        for i in range(1,pixels-2):
            pos[i] = pos[i] + vel[i]*dt;
        data_child.send(pos)

class WavePattern:
    def __init__(self,num_boards = 83):
        self.num_boards = num_boards
        self.data = np.zeros(num_boards*2)
        
    def start_wave(self):
        print "starting wave"
        self.data_parent, data_child = Pipe(duplex=False)
        input_parent, self.input_child = Pipe(duplex=False)
        
        proc = Process(target = make_wave,
                args=(self.num_boards*2,input_parent,data_child))
        proc.daemonic = True
        proc.start()

    def get_line(self):
        while self.data_parent.poll():
            self.data = self.data_parent.recv()
        out = np.zeros((self.num_boards*2,3))
        for i in range(len(out)):
            # new_point = abs(self.data[i])
            new_point = self.data[i]
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
        self.start_wave()
        start_data = np.array(\
                [0]+\
                [0]*(self.num_boards-11)+\
                [1]*20+\
                [0]*(self.num_boards-11)+\
                [0])

        # start_data = np.zeros(self.num_boards*2)
        # for i in range(len(start_data)):
            # start_data[i] = np.sin(i*np.pi*2/(self.num_boards*2-1))

        self.input_child.send(start_data)
        return iter(self.get_line,None)

    
    
