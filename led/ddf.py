#!/usr/bin/env python2.6
from __future__ import division

import ledctl, pattern
import serial, Image

class DDF(ledctl.LEDController):
    def __init__(self, devices, framerate=30, start_websocket=True):
        super(DDF, self).__init__(devices, framerate=framerate, 
                                start_websocket=start_websocket)
        
        if not (devices == 'sim' or devices == ['sim']):
            for i in range(len(devices)):
                self.add_writer(DDFWriter(i, devices[i], framerate))
    
class DDFWriter(ledctl.PatternWriter):
    
    def __init__(self, index, device, framerate):
        super(DDFWriter, self).__init__(framerate)
        
        self.device = device
        self.port = None
        self.index = 1
        
        self.flush = False
        
    def open_port(self):
        self.port = serial.Serial(port=self.device,
                baudrate=57600,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                timeout=0.5,
                writeTimeout=0)
        self.blank()
    
    def close_port(self):
        self.blank()
        self.port.close()
    
    def write(self, o):        
        if type(o) == int:
            self.port.write(chr(o))
        else:
            self.port.write(o)
        
        if self.flush:
            self.port.flush()
        
        #result = self.port.read(self.port.inWaiting())
    
    def draw_frame(self, frame):
        self.write(0x10)
        offset = self.index*4
        map(self.write, frame[offset:offset+4])
    
    def blank(self):
        self.write(0x40)
    
    def red(self):
        self.write(0x10)
        self.write(("\x00"*8+"\xff"*16)*4)
    
    def green(self):
        self.write(0x10)
        self.write(("\xff"*8+"\x00"*8+"\xff"*8)*4)
    
    def blue(self):
        self.write(0x10)
        self.write(("\xff"*16+"\x00"*8)*4)
    
    def reset(self):
        self.write(0x60)

class DDFPattern:
    def __init__(self, filename):
        self.filename = filename
        
        self.frames = []
        self.currentFrame = 0
        
        if filename.endswith('.ddf'):   # Old style DDF pattern, no image headers
            self.read_ddf_pattern()
        else:
            self.read_image()
    
    def read_image(self):
        image = Image.open(self.filename)
        
        image = image.resize((16, 32), Image.ANTIALIAS)
        (width, height) = image.size
        
        image = image.convert('RGB')
        
        try:
            while True:
                frame = image.getdata()
                enc_frame = []
                for r in range(height):
                    row_pix = [frame[i] for i in range(r*width, (r+1)*width)]
                    row_r = nib_encode( [p[0] for p in row_pix] )
                    row_g = nib_encode( [p[1] for p in row_pix] )
                    row_b = nib_encode( [p[2] for p in row_pix] )
                    
                    row = row_r + row_g + row_b
                    enc_frame.append(bytearray(row))
                
                self.frames.append(enc_frame)
                image.seek(image.tell()+1)
        
        except EOFError:
            pass
    
    def __getitem__(self, i):
        return self.frames[i]
                    
    def __iter__(self):
        return iter(self.frames)
                    
def nib_encode(row):
    return [255 - ((row[i] & 0xf0) | (row[i+1] >> 4)) for i in range(0, len(row), 2)]
        