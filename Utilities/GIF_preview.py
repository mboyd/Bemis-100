from __future__ import division

import Image
import numpy as np
import os

def makePreview(inFile,outFile = None):
    '''Make an animated .gif preview of an image for the Bemis100'''
    if outFile == None:
        outFile = 'preview_'+inFile
    tempFolder = inFile+'_temp'
    if os.path.exists(tempFolder):
        print "That filename already has a temporary folder. I'm not sure how that happened. Aborting..."
        return
    os.mkdir(tempFolder)
    im = Image.open(inFile)
    (width,height) = im.size
    for i in range(height):
        out = im.crop([0,i,width,i+1])
        out.resize((800,50),Image.ANTIALIAS).save(\
                os.path.join(tempFolder,format(i,'05d')+'.gif'))
    command ='convert '+'-delay 5 -loop 100 '+os.path.join(tempFolder,'*.gif')+\
            ' ' + outFile
    print command
    os.system(command)
    os.system('rm -r '+tempFolder)

if __name__=='__main__':
    inFolder = '../../../Patterns/Patterns_to_play'
    outFolder = '../../../Patterns/Previews'
    for fn in os.listdir(inFolder):
        if fn[-3:] == 'gif' or fn[-3:] == 'png':
            if fn[-3:] == 'png':
                outFile = os.path.join(outFolder,'preview_'+fn[:-3]+'gif')
            else:
                outFile = os.path.join(outFolder,'preview_'+fn)
            makePreview(os.path.join(inFolder,fn),outFile)
