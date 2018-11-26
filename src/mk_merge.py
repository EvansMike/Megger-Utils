#!/bin/env python

import csv
import database
from datetime import datetime
import logging
import serial
import sys
import time
import xlwt

date = None
wild = None
date = sys.argv[1]
try: wild = sys.argv[2]
except:pass

logging.basicConfig(format='%(module)s: LINE %(lineno)d: %(levelname)s: %(message)s', level=logging.DEBUG)
#logging.disable(logging.INFO)
DEBUG = logging.debug
INFO = logging.info



flab = open('label_merge.csv', 'w')
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
