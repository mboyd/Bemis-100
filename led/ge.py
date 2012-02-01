from __future__ import division

import ledctl, pattern
import serial
import time

class GEController(ledctl.LEDController):
    def __init__(self, device, framerate=20, num_lights=50, start_websocket=True):
        super(GEController, self).__init__(device, framerate=framerate, 
                                    start_websocket=False)
        
        self.num_lights = num_lights
        if not device == 'sim':
            self.add_writer(GEWriter(device, num_lights, framerate))

class GEWriter(ledctl.PatternWriter):
    
    def __init__(self, device, num_lights, framerate):
        super(GEWriter, self).__init__(framerate)
        
        self.device = device
        self.port = None
        self.num_lights = num_lights
        self.last_frame = None

    def open_port(self):
        self.port = serial.Serial(port=self.device,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                timeout=0.5,
                writeTimeout=0)
        time.sleep(3)
        self.blank()

    def close_port(self):
        self.blank();
        self.port.close()
        print "Port closed"

    def draw_frame(self, frame):
        # self.port.write('B')
        for i in range(0, len(frame), 3):
            if self.last_frame is None or frame[i:i+3] != self.last_frame[i:i+3]:
                self.port.write(chr(i//3) + frame[i:i+3])
                time.sleep(.0012) #give the controller enough time to write the new data
        self.last_frame = frame
 
    def blank(self):
        '''Turn off all the LEDs. We do this before startup to make sure the
        power supplies are not loaded by the LEDs when they come online.'''
        print self.num_lights
        f = bytearray('\x00\x00\x00'*self.num_lights)
        self.draw_frame(f)
 
