from __future__ import division

import Image as im
import os


inFolder = '../Patterns/Lines/166x166'
outFolder = '../Patterns/Lines/onBlack/'

for fn in os.listdir('.'):
    if fn[-3:] =='gif':
        print fn
        img = im.open(fn)
        source = img.split()
        R,G,B = 0,1,2
        mask = source[G].point(lambda i: i > 100 and 255)
        out = source[G].point(lambda i: 0)
        source[G].paste(out,None,mask)
        
        img_out = Image.merge(img.mode,source)
        outfile = outFolder+afn+'_on_black'
        img_out.save(outfile,'GIF')
    
    

