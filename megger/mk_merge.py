#!/bin/env python
'''
Make a merge file to be used with glables to print on a Brother label printer.
Output a csv file with the data relevant from the supplied date.
Useage: mk_merge.py 2018-11-22 <string>
An optional string can be supplies as a search string to restrict the returned results.

'''

import csv
import database
from datetime import datetime
import logging
import serial
import sys
import time

date = None
wild = None
try:
    date = sys.argv[1]
except:
    date = datetime.today().strftime('%Y-%m-%d') # Default to today
try:
    wild = sys.argv[2]
except:
    pass

logging.basicConfig(format='%(module)s: LINE %(lineno)d: %(levelname)s: %(message)s', level=logging.DEBUG)
#logging.disable(logging.INFO)
DEBUG = logging.debug
INFO = logging.info

def main():
    flab = None
    if wild: flab = open('label_merge-'+ date + '_' + wild + '.csv', 'w')
    else: flab = open('label_merge-'+ date + '.csv', 'w')
    db = database.Database()
    DEBUG(date)
    if wild: data = db.get_merge_info(str(date), wild)
    else: data = db.get_merge_info(str(date))
    DEBUG(data)
    try:
        for line in data:
            flab.write(str(line['asset_id']) + ',"' + str(line['test_date']) \
                + '","' + str(line['next_date']) + '"\n' )
    except:
        pass
    flab.close()

if __name__ == '__main__':
    main()
