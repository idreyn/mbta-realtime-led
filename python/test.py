from map import *
from bitpusher import *
from data import *

import time

a = ArduinoBridge()
time.sleep(1)

if True:
    writes = []
    for route in ROUTE_SEGMENTS:
        color = ROUTE_COLORS[route]
        for seg in ROUTE_SEGMENTS[route]:
            sw = StripWrite(
                STRIPS[seg[0]][0],
                seg[1],
                seg[2],
                color
            )
            writes.append(sw)
    a.write(writes)
