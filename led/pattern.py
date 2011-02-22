#!/usr/bin/env python2.6
from __future__ import division

import Image as im

'''This program generates patterns for the Bemis100 lighting system. A pattern
is derived from an image file, which will be played back one row at a time on
the Bemis100. 
'''

class Bemis100Pattern:
    def __init__(self, filename, num_boards=0):
        self.filename = filename
        self.current_row = 0
        self.read_image(2*num_boards)

    def read_image(self, target_width=0):
        '''Read the image, then create an array with the data in the correct
        format for the Bemis100.'''
        image = im.open(self.filename)
        (width,height)=image.size

        if not target_width == 0:
            image = image.resize((int(target_width), height), im.ANTIALIAS)
            (width,height) = image.size

        image = image.convert('RGB')
        
        self.image_data = []
        
        try:
            while True:
                frame = image.getdata()
                for r in range(height):
                    row_pix = (frame[i] for i in range(r*width, (r+1)*width))
                    row_raw = (b for pix in row_pix for b in pix)
                    row = bytearray((encode_char(c) for c in row_raw))
                    
                    self.image_data.append(row)
                
                image.seek(image.tell()+1)
        
        except EOFError:
            pass
            
    def __iter__(self):
        return iter(self.image_data)

#
# PWM Routines
#

PWM_BITS = 8
PWM_BINS = PWM_BITS + 1
PWM_CUTOFFS = [int(round(255.*i/(PWM_BINS))) for i in range(1, PWM_BINS+1)]
PWM_VALS = [2**i-1 for i in range(PWM_BINS)]

def encode_char(value):
    return PWM_LOOKUP[int(value)]

def _encode_char(value):
    """Return a bitmask for a pwm representation of the 8-bit
    integer value. Our firmware only implements 8 shades, so we indicate the
    brightness of a pixel by the number of 1s in an 8-bit string, which we
    transmit as a single character."""
    
    for i in range(PWM_BINS):
        if value <= PWM_CUTOFFS[i]:
            return PWM_VALS[i]
    raise ValueError, "Pixel value %i out of range" % value

PWM_LOOKUP = [_encode_char(i) for i in range(256)]

def decode_char(x):
    '''Undo the conversion from char values to bytes, in which the value is
    indicated by the number of 1s in the byte'''
    return PWM_DECODE_LOOKUP[x]

PWM_DECODE_LOOKUP = {PWM_VALS[0] : 0}
for i in range(1, PWM_BINS-1):
    PWM_DECODE_LOOKUP[PWM_VALS[i]] = int(round((PWM_CUTOFFS[i] - PWM_CUTOFFS[i-1]) / 2 + PWM_CUTOFFS[i-1]))
PWM_DECODE_LOOKUP[PWM_VALS[-1]] = 255
