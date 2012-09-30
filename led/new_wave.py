from __future__ import division

from wave import WavePattern

class NewWavePattern(WavePattern):
    def output_func(self, point):
        if point > 1:
            point = 1
        elif point < -1:
            point = -1
        # return [int(127 - point*127), 0, int(127 + point*127)]
        
        if point > 0:
            return [int(255 * point), 0, 0]
        else:
            return [int(255 * -point), int(85 * -point), 0]
        
