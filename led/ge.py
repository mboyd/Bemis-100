from __future__ import division

import ledctl, pattern
import serial
import time


ACK_COUNT = 4

class GEController(ledctl.LEDController):
    def __init__(self, device, framerate=60, num_lights=50, start_websocket=True):
        super(GEController, self).__init__(device, framerate=framerate, 
                                    start_websocket=start_websocket)
        
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
                timeout=2,
                writeTimeout=0)
        time.sleep(3)
        self.bytes_since_ack = 0
        self.blank()

    def close_port(self):
        self.blank();
        self.port.close()
        print "Port closed"

    def draw_frame(self, frame):
        # self.port.write('B')
        for i in range(0, len(frame), 3):
            if self.last_frame is None or frame[i:i+3] != self.last_frame[i:i+3]:
                to_write = chr(i//3) + frame[i:i+3]
                self.port.write(to_write)
                # print "written", count
                # self.port.read(1)
                self.bytes_since_ack += 4
                if self.bytes_since_ack >= ACK_COUNT:
                    # print "waiting for ack"
                    c = self.port.read(1)
                    # print ord(c)
                    self.bytes_since_ack = 0
                    assert c == 'B', c
                    # c = self.port.read(1)
                    # assert c == '', c
                # time.sleep(.0012) #give the controller enough time to write the new data
        self.last_frame = frame
 
    def blank(self):
        return
        '''Turn off all the LEDs. We do this before startup to make sure the
        power supplies are not loaded by the LEDs when they come online.'''
        print self.num_lights
        f = bytearray(reduce(str.__add__, [chr(i) + '\x00\x00\x00' for i in range(self.num_lights)]))
        print repr(f)
        self.draw_frame(f)
 
