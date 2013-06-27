from __future__ import division

import multiprocessing
import time
import RPi.GPIO as GPIO
import ledctl
import time
import numpy as np
import itertools

GPIO.setmode(GPIO.BCM)
PIN = 18
GPIO.setup(PIN, GPIO.OUT)


class RaspberryPiWriter(ledctl.PatternWriter):
    def __init__(self, device, num_lights=50, framerate=30):
        super(RaspberryPiWriter, self).__init__(framerate)

        self.num_lights = num_lights

    def open_port(self):
        pass

    def write_bit(self, b):
        if b:
            off_time = 20 / 1e6
            on_time = 10 / 1e6
        else:
            off_time = 10 / 1e6
            on_time = 20 / 1e6
        # timer1 = timer.Timer(off_time, lambda: GPIO.output(PIN, True))
        # timer2 = timer.Timer(on_time, lambda: GPIO.ouput(PIN, False))
        GPIO.output(PIN, False)
        # timer1.start()
        time.sleep(off_time)
        GPIO.output(PIN, True)
        time.sleep(on_time)
        GPIO.output(PIN, False)

    def write_begin(self):
        GPIO.output(PIN, True)
        time.sleep(10/1e6)
        GPIO.output(PIN, False)

    def write_end(self):
        GPIO.output(PIN, False)
        time.sleep(40/1e6)

    def set_color(led, intensity, color):
        addr_b = np.unpackbits(np.array([led], dtype=np.uint8))[2:]
        intensity_b = np.unpackbits(np.array([intensity], dtype=np.uint8))
        color_b = itertools.chain(*[np.unpackbits(np.array([c>>4], dtype=np.uint8))[4:] for c in reversed(color)])
        self.write_begin()
        for b in itertools.chain(addr_b, intensity_b, color_b):
            self.write_bit(b)
        self.write_end()

    def fill_color(self, begin, count, intensity, color):
        for i in range(count):
            self.set_color(begin, intensity, color)
            begin += 1






