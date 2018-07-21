#!/bin/env python

import serial
import time
import csv


class Test(object):
    def __init__(self, data_csv):

        return


class Asset(object):
    def __init__(self, data_csv):
        self.id = data_csv[1]
        self.name = data_csv[3]
        self.serial = data_csv[5]
        self.tests = []
        return


class Megger(object):
    def __init__(self):
        self.assets = []
        self.tests = []
        data = self.download()
        self.save_to_file(data)
        self.parse_data(data)
        return

    def parse_data(self, data):
        for line in data:
            data_csv = line.split(',')
            #print data_csv
            #if data_csv == 'C':
            #    asset = Assest(data_csv)
            #    self.assets.append(asset)
            if data_csv == 'D':
                asset = Assest(data_csv)
                self.assets.append(asset)
            if data_csv == 'A':
                test = Test(data_csv)
                self.tests.append(test)

    def save_to_file(self, data):
        fid = open('megger.csv', 'w')
        for line in data:
            fid.write(line + '\n')
        fid.close()
        return

    def download(self):
        '''
        Download the date from the PAT4
        TODO; Don't hardcode the port.
        '''
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
        return data

def main():
    megger = Megger()





if __name__ == '__main__':
    main()
