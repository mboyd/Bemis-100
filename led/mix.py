import sys
import random
import time

sys.path.append('..')
from led.pattern import Bemis100Pattern
from led.utils import find_patterns_flat

class MixPattern:
    def __init__(self, folder, num_lights=50):
        self.folder = folder
        self.num_lights = num_lights
        self.pattern_paths = find_patterns_flat(folder)
        self.patterns = []
        self.build_patterns()

    def build_patterns(self):
        for p in self.pattern_paths:
            pat = Bemis100Pattern(p, self.num_lights)
            self.patterns.append(pat)

    def __iter__(self):
        return MixPattern.shuffle(*self.patterns)

    @staticmethod
    def shuffle(*iters):
        while True:
            p = iters[random.randrange(0, len(iters))]
            n = random.randrange(1,3)
            start_time = time.time()
            timed_out = False
            for j in range(n):
                for x in p:
                    yield x
                    if time.time() - start_time > 120:
                        timed_out = True
                        break
                if timed_out:
                    break
