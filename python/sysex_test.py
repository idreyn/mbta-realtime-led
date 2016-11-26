from pyfirmata import Board, util, boards
from random import randint
import math

PORT = '/dev/cu.usbmodem1411'


def test_handle(*data):
	print list(data[::2])

b = Board(PORT, boards.BOARDS['arduino'], 57600)
b.add_cmd_handler(0x71, test_handle)

random_strings = []
for i in xrange(10):
	r = map(lambda x: randint(0, 127), xrange(8))]
	print r
	s = ''.join(map(lambda x: chr(x), r))
	b.send_sysex(0x71, util.str_to_two_byte_iter(s))

print '================='

b.pass_time(2)

while b.bytes_available():
	b.iterate()
