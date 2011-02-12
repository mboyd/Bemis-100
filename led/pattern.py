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
            image = image.resize((target_width, height), im.ANTIALIAS)
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


def encode_char(value):
    """Return a sequence of boolean states for a pwm representation of the 8-bit
    integer value. Our firmware only implements 8 shades, so we indicate the
    brightness of a pixel by the number of 1s in an 8-bit string, which we
    transmit as a single character."""
    
    # FIXME: Really?
    
    raw = reduce(lambda x,y: x+y,
            map(lambda x: str(int(x)),
                [value>=255*i/8. for i in range(1,9)]))
    # raw = str(int(value>=255*1))+\
            # str(int(value>=255*7/8))+\
            # str(int(value>=255*6/8))+\
            # str(int(value>=255*5/8))+\
            # str(int(value>=255*4/8))+\
            # str(int(value>=255*3/8))+\
            # str(int(value>=255*2/8))+\
            # str(int(value>=255*1/8))
    return int(raw,2)

def decode_char(x):
    '''Undo the conversion from char values to bytes, in which the value is
    indicated by the number of 1s in the byte'''
    return int(bin(x).count('1') * 255/8)
