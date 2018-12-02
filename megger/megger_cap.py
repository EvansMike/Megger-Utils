#!/bin/env python
#  megger_cap.py
#
#  Copyright 2018 Mike Evans <mikee@saxicola.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import csv
import database
from datetime import datetime
import logging
import serial
import time
import xlwt

logging.basicConfig(format='%(module)s: LINE %(lineno)d: %(levelname)s: %(message)s', level=logging.DEBUG)
#logging.disable(logging.INFO)
DEBUG = logging.debug
INFO = logging.info

class Megger(object):
    def __init__(self):
        self.assets = []
        self.tests = []
        data = self.download()
        self.write_xls(data)
        return

    def store_data(self,data):


        return

    def write_xls(self, data):
        db = database.Database()
        wb = xlwt.Workbook()
        ws1 = wb.add_sheet("Assets")
        ws2 = wb.add_sheet("Results")
        #ws3 = wb.add_sheet("Sites")
        assets_header = ["Assets", "Asset #", "Site","Asset ID", "Test", "Serial #", "Name", \
            "Location", "TestDate", "Next Date", "TBT months", "VA", "?"]
        for c, heading in enumerate(assets_header):
            ws1.write(0,c,heading)
        tests_header = ["Results", "Asset ID","Test Date","Test Time","User #","","","EB1","EB2", \
            "EB3","Insulation M","VA", "E Leakage", "", "Fault #", "Repair#"]
        for c, heading in enumerate(tests_header):
            ws2.write(0,c,heading)
        a = 0
        d = 0
        s = 0
        assets_dict = {} # Number to ID mapping
        sites_dict = {} #
        for drow in data:
            if drow.startswith('S,'): #  Sites
                s += 1
                srow = drow.split(',')
                sites_dict[srow[1]]  = srow[4]
            if drow.startswith('D,'): #  Assets
                db.add_asset(drow)
                d += 1
                srow = drow.split(',')
                if srow[2] in sites_dict:
                    srow[2] = sites_dict[srow[2]]
                assets_dict[srow[1]]  = srow[3]
                for j, col in enumerate(tuple(srow)):
                    # Fix date strings
                    if j == 8:
                        col = datetime.strptime(col, '%d%m%y').strftime("%Y-%m-%d")
                    if j == 9:
                        col = datetime.strptime(col, '%d%m%y').strftime("%Y-%m-%d")
                    ws1.write(d, j, col)

            elif drow.startswith('A,'): # Test results
                db.add_result(drow)
                a += 1
                srow = drow.split(',')
                if srow[1] in assets_dict:
                    srow[1] = assets_dict[srow[1]]
                for j, col in enumerate(tuple(srow)):
                    # Fix date strings
                    if j == 2:
                        col = datetime.strptime(col, '%d%m%y').strftime("%Y-%m-%d")
                    ws2.write(a, j, col)
        if a > 0:
            wb.save("megger_data.xls")
            self.save_to_file(data)
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
