from __future__ import division

from multiprocessing import Process, Pipe
from wave import WavePattern
import pattern
import numpy as np
import random

class NewWavePattern(WavePattern):
    def output_func(self, point):
        if point > 1:
            point = 1
        elif point < -1:
            point = -1
        return [int(127 - point*127), 0, int(127 + point*127)]
        
        
