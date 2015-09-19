import time
import serial

PORT = '/dev/cu.usbmodem1411'

class ArduinoBridge(object):
	def __init__(self):
		self.port = serial.Serial(PORT,115200)
	def reset():
		self.port.write(char(0xFE))
		time.sleep(0.1)

	def write(self,updates):
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
		for o in out:
			self.port.write(chr(o))
		self.port.write(chr(0xFF))
		time.sleep(0.08)