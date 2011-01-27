#!/usr/bin/env python2.6
from __future__ import division

import numpy as np
import re
import Image as im

'''This program generates patterns for the Bemis100 lighting system. A pattern
is derived from an image file, which will be played back one row at a time on
the Bemis100. 
'''

class Bemis100Pattern:
    def __init__(self, filename, num_boards=None):
        self.filename = filename
        self.read_image(2*num_boards)

    def read_image(self, target_width=None):
        '''Read the image, then create an array with the data in the correct
        format for the Bemis100.'''
        image = im.open(self.filename)
        (width,height)=image.size
        
        if not target_width == None:
            image = image.resize((target_width, height), im.ANTIALIAS)
            (width,height) = image.size

        rgbim = image.convert('RGB')
        data = np.array([([output_char(c) for c in p]) for p in rgbim.getdata()])
        self.image_data = data.reshape((-1,width,3))

        # This section is used to load frames from an animated .gif which is
        # passed to the pattern generator. It seeks to each frame in the file
        # and adds whatever data is found there to the current pattern. When the
        # end of the file is reached, an EOFError is raised.
        try:
            while 1:
                image.seek(image.tell()+1)
                rgbim = image.convert('RGB')
                (width,height)=rgbim.size
                data = np.array([([output_char(c) for c in p]) for p in rgbim.getdata()])
                self.image_data = np.vstack((self.image_data,\
                        np.array(list(data)).reshape((-1,width,3))))
        except EOFError:
            pass

def output_char(value):
    """Return a sequence of boolean states for a pwm representation of the 8-bit
    integer value. Our firmware only implements 8 shades, so we indicate the
    brightness of a pixel by the number of 1s in an 8-bit string, which we
    transmit as a single character."""
    raw = str(int(value>=255*1))+\
            str(int(value>=255*7/8))+\
            str(int(value>=255*6/8))+\
            str(int(value>=255*5/8))+\
            str(int(value>=255*4/8))+\
            str(int(value>=255*3/8))+\
            str(int(value>=255*2/8))+\
            str(int(value>=255*1/8))
    return int(raw,2)
