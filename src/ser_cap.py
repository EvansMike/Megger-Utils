#!/bin/env python

import serial
import time
import csv

assets = []
asset = {}
tests = []
test = {}

def do_asset(data):
    return


ser = serial.Serial('/dev/ttyS5')
ser.dsrdtr = 1 # Enable hardware (RTS/CTS) flow control.
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.stopbits = serial.STOPBITS_ONE
ser.parity = serial.PARITY_EVEN
ser.timeout = 1.1
try:
    ser.open()
except:
    pass
ser.flushInput()
data = []
ser.write('s\r'.encode())
line = ser.readline().decode("utf-8").replace('\r\n', "")
data.append(line)
print line
while line:
    ser.write('\r'.encode())
    line = ser.readline().decode("utf-8").replace('\r\n', "")
    if line:
        data.append(line)
        print line
    else:
        break
ser.close()

print "data follows:"
for line in data:
    csv = line.split(',')
    if line[0] = 'D':
        do_asset(line)


