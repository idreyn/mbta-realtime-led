import time
import serial
import sys
import threading
import random

PORT = '/dev/cu.usbmodem1411'

ser = serial.Serial(PORT, 9600)
print 'wait...'
time.sleep(4)

start_time = time.time()
data = []


def read_input(ser, lock):
    read_index = 0
    print 'waiting on serial input'
    sys.stdout.flush()
    while True:
        next = int(ord(ser.read()))
        next_write = data[read_index]
        # print hex(next), hex(next_write), len(data),
        # ','.join(map(hex,data[-10:]))
        lock.acquire()
        assert next == next_write
        sys.stdout.flush()
        read_index = read_index + 1
        lock.release()


def write_output(ser, lock):
    print 'writing to serial'
    sys.stdout.flush()
    while True:
        for i in xrange(8 * 500):
            rand = random.randint(0, 126)
            data.append(rand)
            ser.write(chr(rand))
        lock.acquire()
        data.append(0xFF)
        ser.write(chr(0xFF))
        lock.release()
        time.sleep(0.05)


def clock_output():
    while True:
        time.sleep(1)
        print int(len(data) / (time.time() - start_time)), 'Bps'

if __name__ == '__main__':
    read_lock = threading.Lock()
    read = threading.Thread(target=read_input, args=(ser, read_lock))
    read.start()
    write = threading.Thread(target=write_output, args=(ser, read_lock))
    write.start()
    clock = threading.Thread(target=clock_output)
    clock.start()
    write.join()
    read.join()
