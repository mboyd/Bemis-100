#!/usr/bin/env python2.6
from __future__ import division

import Image as im

'''This program generates patterns for the Bemis100 lighting system. A pattern
is derived from an image file, which will be played back one row at a time on
the Bemis100. 
'''

class Bemis100Pattern:
    def __init__(self, filename, num_boards=None):
        self.filename = filename
        self.current_row = 0
        self.read_image(2*num_boards)

    def read_image(self, target_width=None):
        '''Read the image, then create an array with the data in the correct
        format for the Bemis100.'''
        image = im.open(self.filename)
        (width,height)=image.size

        if not target_width == None:
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
                    row = bytearray((output_char(c) for c in row_raw))
                    
                    self.image_data.append(row)
                
                image.seek(image.tell()+1)
        
        except EOFError:
            pass
            
    def __iter__(self):
        return iter(self.image_data)


def output_char(value):
    """Return a sequence of boolean states for a pwm representation of the 8-bit
    integer value. Our firmware only implements 8 shades, so we indicate the
    brightness of a pixel by the number of 1s in an 8-bit string, which we
    transmit as a single character."""
    
    # FIXME: Really?
    
    raw = str(int(value>=255*1))+\
            str(int(value>=255*7/8))+\
            str(int(value>=255*6/8))+\
            str(int(value>=255*5/8))+\
            str(int(value>=255*4/8))+\
            str(int(value>=255*3/8))+\
            str(int(value>=255*2/8))+\
            str(int(value>=255*1/8))
    return int(raw,2)
