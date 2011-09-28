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
                    row = bytearray((c for c in row_raw))
                    
                    self.image_data.append(row)
                
                image.seek(image.tell()+1)
        
        except EOFError:
            pass
            
    def __iter__(self):
        return iter(self.image_data)


