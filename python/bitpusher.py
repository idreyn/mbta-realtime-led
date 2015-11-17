import time
import serial

PORT = '/dev/ttyACM0'

class ArduinoBridge(object):
    def __init__(self):
        self.port = serial.Serial(PORT,115200)

    def reset():
    	self.port.write(char(0xFE))
    	time.sleep(0.1)

    def write(self,updates,elapsed=0):
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
        self.port.write(''.join(map(chr,out)))
        self.port.write(chr(0xFF))
        sleep_time = 0.010
        time.sleep(sleep_time)
