import ConfigParser
from datetime import datetime
import logging
import MySQLdb
import MySQLdb.cursors
import os
import warnings


home = os.environ['HOME']
config_file = home + "/.megger.cfg"
config = ConfigParser.ConfigParser()
config.read(config_file)
warnings.filterwarnings('ignore', category=MySQLdb.Warning)
DEBUG = logging.debug
INFO = logging.info

# Could use ON DUPLICATE KEY UPDATE

class Database(object):
    def __init__(self):
        db_user = config.get('database','USER')
        db_pass = config.get('database','PASSWD')
        db_base = config.get('database','DB')
        db_host = config.get('database','DBHOST')

        self.db = MySQLdb.connect(host=db_host, user=db_user, password=db_pass, database=db_base)
        self.cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        return

    def add_asset(self,asset):
        '''
        Db fields are
        "Asset #", "Site","Asset ID", "Test", "Serial #", "Name", \
            "Location", "TestDate", "Next Date", "TBT months", "VA", "?"
        '''
        to_insert = asset.split(',')
        # Fix the date string
        DEBUG(str(to_insert[8]))
        to_insert[8] = datetime.strptime(str(to_insert[8]), '%d%m%y').strftime("%Y-%m-%d")
        to_insert[9] = datetime.strptime(str(to_insert[9]), '%d%m%y').strftime("%Y-%m-%d")
        # Insert ignoring duplicate keys
        self.cur.execute("INSERT IGNORE INTO assets(asset_num, site,asset_id, \
            test, serial, name, location, test_date, next_date, test_interval, VA, m1) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            (to_insert[1],to_insert[2],to_insert[3],to_insert[4],to_insert[5],\
            to_insert[6],to_insert[7],to_insert[8],to_insert[9],to_insert[10], \
            to_insert[11],to_insert[12]))
        self.db.commit()


    def add_result(self, result):
        '''
        '''
        to_insert = result.split(',')
        # Fix the date string
        DEBUG(str(to_insert[2]))
        to_insert[2] = datetime.strptime(str(to_insert[2]), '%d%m%y').strftime("%Y-%m-%d")
        # Insert ignoring duplicate keys
        self.cur.execute("INSERT IGNORE INTO results(asset_num,test_date, test_num, user_num, \
            m1, m2, e_bond_1, e_bond_2, m3, insulation, VA, e_leakage, m4, fault_num, repair_num ) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            (to_insert[1],to_insert[2],to_insert[3],to_insert[4],to_insert[5], \
            to_insert[6],to_insert[7],to_insert[8],to_insert[9],to_insert[10], \
            to_insert[11],to_insert[12],to_insert[13],to_insert[14],to_insert[15]))
        self.db.commit()


    def create_tables(self):
        return
