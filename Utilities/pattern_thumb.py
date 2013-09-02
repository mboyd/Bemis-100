from __future__ import division

import PIL.Image as Im
import sys

def makePatternThumb(inFile, outFile):
    """
    Make a 150x150 thumbnail of a pattern image
    """
    im = Im.open(inFile)
    im.resize((150,150), Im.ANTIALIAS).save(outFile)

if __name__ == '__main__':
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    makePatternThumb(inFile, outFile)
