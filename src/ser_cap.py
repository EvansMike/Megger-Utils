#!/bin/env python

import serial
import time
import csv
import xlwt


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
        self.write_xls(data)
        return

    def write_xls(self, data):
        wb = xlwt.Workbook()
        ws1 = wb.add_sheet("Assets")
        ws2 = wb.add_sheet("Results")
        assets_header = ["Results", "Asset#", "","Asset ID", "Test", "Serial#", "Name", \
            "Location", "TestDate", "Next Date", "TBT months", "VA", "?"]
        for c, heading in enumerate(assets_header):
            ws1.write(0,c,heading)
        tests_header = ["Results", "Asset#","Test Date","","","","","Earth","Bond", \
            "","Insulation M","VA", "E Leakage", "", "", "Repair#"]
        for c, heading in enumerate(tests_header):
            ws2.write(0,c,heading)
        a = 0
        d = 0
        for drow in data:
            if drow.startswith('D,'):
                d += 1
                srow = drow.split(',')
                for j, col in enumerate(tuple(srow)):
                    ws1.write(d, j, col)
            elif drow.startswith('A,'):
                a += 1
                srow = drow.split(',')
                for j, col in enumerate(tuple(srow)):
                    ws2.write(a, j, col)

        wb.save("megger_data.xls")
        return

    def parse_data(self, data):
        for line in data:
            #data_csv = line.split(',')

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
