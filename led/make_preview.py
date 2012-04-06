from __future__ import division

from new_wave import NewWavePattern
from wave import WavePattern
"""
Designed to draw a preview image of a dynamic pattern (running this on a static pattern should produce the image used to generate that pattern.
"""

import Image as im
import numpy as np

def extract_rows(pattern, num_rows):
    pattern_data = []
    row_ndx = 0
    for row in pattern:
        row_data = [ord(chr(x)) for x in row]
        row_data_grouped = [row_data[i:i+3] for i in range(0, len(row)-3, 3)]
        # print row_data_grouped
        pattern_data.append(row_data_grouped)
        row_ndx += 1
        if row_ndx >= num_rows:
            break
    return pattern_data

def save_preview(data, filename):
    width = len(data[0])
    height = len(data)
    image = im.fromarray(np.array(data, np.uint8))
    # image.show()
    image.save(filename)

if __name__ == "__main__":
    save_preview(extract_rows(NewWavePattern(num_lights=201), 1000), "wave.png")


    
