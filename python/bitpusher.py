import time
import serial
from data import *


class ArduinoBridge(object):

    def __init__(self):
        for port in PORTS:
            try:
                print 'connecting to', port
                self.port = serial.Serial(port, 115200)
            except:
                print 'failed to connect'
                continue
            break

    def write(self, updates, elapsed=0):
        out = []
        for w in updates:
            next = [
                w.index,
                (w.start >> 8) & 0xFF,
                w.start & 0xFF,
                (w.end >> 8) & 0xFF,
                w.end & 0xFF,
                (w.color >> 16) & 0xFF,
                (w.color >> 8) & 0xFF,
                w.color & 0xFF,
            ]
            out = out + next
        t0 = time.time()
        self.port.write(''.join(map(chr, out)))
        self.port.write(chr(0xFF))
        time.sleep(SLEEP_TIME)
