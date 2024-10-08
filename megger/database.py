#  database.pyll
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
'''
Database malarky for megger_cap(ture)
I really should use sqlite more for this sort of thing as it's not always trivial
to set up a MySQL database for potential users.
'''

import sys
py_version = sys.version_info.major
if py_version == 2:
    import ConfigParser
if py_version == 3:
    import configparser as ConfigParser
from datetime import datetime
import logging
import MySQLdb
import MySQLdb.cursors
import os
import warnings

warnings.filterwarnings('ignore', category=MySQLdb.Warning)
DEBUG = logging.debug
INFO = logging.info

# Could use ON DUPLICATE KEY UPDATE

class Database(object):
    def __init__(self):
        home = os.environ['HOME']
        config_file = home + "/.megger.cfg"
        config = ConfigParser.ConfigParser()
        #config = configparser.ConfigParser()
        try:
            config.read(config_file)
        except:
            print ('No configuration file present, or malformed file')
            quit(1)
        db_user = config.get('database','USER')
        db_pass = config.get('database','PASSWD')
        db_base = config.get('database','DB')
        db_host = config.get('database','DBHOST')

        self.db = MySQLdb.connect(host=db_host, user=db_user, password=db_pass, database=db_base)
        self.cur = self.db.cursor(MySQLdb.cursors.DictCursor)
        return


    def add_site(self, data):
        '''
        S,6,3,"","HERE","17 CHURCH STREET","NARBERT","SA67 7BH
        Bug-363 TODO
        '''
        to_insert = data.split(',')
        try:
            self.cur.execute("INSERT INTO sites(site_num, client_num, m1, site_name, addr_1, addr_2, addr_3) \
                VALUES(%s, %s, %s, %s, %s, %s, %s)", \
                (to_insert[1], to_insert[2], to_insert[3].strip('"'), to_insert[4].strip('"'), to_insert[5].strip('"'), to_insert[6].strip('"'), to_insert[7].strip('"')))
            print ("Adding new site")
        except MySQLdb.Error as e: # Or update the site with new data.
            print(str(e))
            self.cur.execute("UPDATE sites SET m1 = %s, site_name = %s, addr_1 = %s, addr_2 = %s, addr_3 = %s  \
                WHERE site_num = %s", \
                (to_insert[3].strip('"'), to_insert[4].strip('"'), to_insert[5].strip('"'), to_insert[6].strip('"'), to_insert[7].strip('"'), to_insert[1].strip('"')))
        self.db.commit()



    def add_client(self, data):
        '''
        C,3,"MILLSTREAM","17 CHURCH STREET","NARBERTH","SA67 7BH"
        '''
        to_insert = data.split(',')
        try:
            self.cur.execute("INSERT INTO clients(client_num, name, addr1, addr2, addr3) VALUES(%s, %s, %s, %s, %s)",\
                (to_insert[1], to_insert[2].strip('"'), to_insert[3].strip('"'), to_insert[4].strip('"'), to_insert[5].strip('"')))
            print ("Adding new client")
        except MySQLdb.Error as e:
            print(str(e))
            self.cur.execute("UPDATE clients SET  name = %s, addr1 = %s, addr2 = %s, addr3 =%s  WHERE client_num = %s", \
            (to_insert[2].strip('"'), to_insert[3].strip('"'), to_insert[4].strip('"'), to_insert[5].strip('"'), to_insert[1].strip('"')))
            print (f"Updating client id: {to_insert[1]}")
        self.db.commit()
        return


    def add_user(self,data):
        '''
        U,2,"MIKEE",0,"6658"
        '''
        to_insert = data.replace('"','').split(',')
        INFO(to_insert)
        try:
            self.cur.execute("INSERT INTO users(id, name, m1, pass) \
                VALUES(%s, %s, %s, %s)",\
                (to_insert[1], to_insert[2], to_insert[3], to_insert[4]))
            print(f"Added user: {to_insert[2]}")
            self.db.commit()
        except MySQLdb.Error as e:
            self.cur.execute("UPDATE users SET name = %s, m1 = %s, pass= %s \
                WHERE id = %s", (to_insert[2], to_insert[3], to_insert[4], to_insert[1]))
            self.db.commit()
        return

    def add_class(self, data):
        '''
        Add or update the  test_classes table
        '''
        to_insert = data.replace('"','').split(',')
        INFO(to_insert)
        try:
            self.cur.execute("INSERT INTO test_classes(id, m1, name, m2, m3, m4, m5, m6, m7, m8) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            (to_insert[1], to_insert[2], to_insert[3], to_insert[4], to_insert[5], \
            to_insert[6], to_insert[7], to_insert[8], to_insert[9], to_insert[10]))
        except MySQLdb.Error as e:
            INFO(str(e))
            self.cur.execute("UPDATE test_classes set m1 = %s, name = %s, m2 = %s, \
                m3 = %s, m4 = %s, m5 = %s, m6 = %s, m7 = %s, m8 = %s WHERE id= %s",\
                (to_insert[2], to_insert[3], to_insert[4], to_insert[5], to_insert[6], \
                to_insert[7], to_insert[8], to_insert[9], to_insert[10], to_insert[1]))
        self.db.commit()


    def add_asset(self,asset):
        '''
        Db fields are
        "Asset #", "Site","Asset ID", "Test", "Serial #", "Name", \
            "Location", "TestDate", "Next Date", "TBT months", "VA", "?"
        '''
        to_insert = asset.split(',')
        # Fix the date string
        #DEBUG(str(to_insert[8]))
        to_insert[8] = datetime.strptime(str(to_insert[8]), '%d%m%y').strftime("%Y-%m-%d")
        to_insert[9] = datetime.strptime(str(to_insert[9]), '%d%m%y').strftime("%Y-%m-%d")
        # Insert ignoring duplicate keys.
        try:
            self.cur.execute("INSERT INTO assets(asset_num, site, asset_id, \
            test, serial, name, location, test_date, next_date, test_interval, VA, m1) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            (to_insert[1],to_insert[2],to_insert[3].strip('"') ,to_insert[4].strip('"'),to_insert[5],\
            to_insert[6],to_insert[7],to_insert[8],to_insert[9],to_insert[10], \
            to_insert[11],to_insert[12]))
            print ("Adding new asset")
        except MySQLdb.Error as e: # Or update the asset with new data.
            #DEBUG(e)
            self.cur.execute("UPDATE assets SET site = %s, asset_id = %s, \
            test = %s, serial = %s, name = %s, location = %s, test_date = %s, next_date = %s, \
            test_interval = %s, VA = %s, m1 = %s WHERE asset_num = %s", \
            (to_insert[2],to_insert[3].strip('"'),to_insert[4].strip('"'),to_insert[5],\
            to_insert[6],to_insert[7],to_insert[8],to_insert[9],to_insert[10], \
            to_insert[11],to_insert[12], to_insert[1]))
            print ("Updating assets")
        self.db.commit()


    def add_result(self, result):
        '''
        '''
        to_insert = result.split(',')
        # Fix the date string
        #DEBUG(str(to_insert[2]))
        to_insert[2] = datetime.strptime(str(to_insert[2]), '%d%m%y').strftime("%Y-%m-%d")
        # Fix the time string
        DEBUG(str(to_insert[3]))
        to_insert[3] = datetime.strptime(str(to_insert[3]), '%H%M').strftime("%H:%M:%S")
        DEBUG(str(to_insert[3]))
        # Insert ignoring duplicate keys
        self.cur.execute("INSERT IGNORE INTO results(asset_num,test_date, test_time, user_num, \
            m1, m2, e_bond_1, e_bond_2, e_bond_3, insulation, VA, e_leakage, m4, fault_num, repair_num ) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            (to_insert[1],to_insert[2],to_insert[3],to_insert[4],to_insert[5], \
            to_insert[6],to_insert[7],to_insert[8],to_insert[9],to_insert[10], \
            to_insert[11],to_insert[12],to_insert[13],to_insert[14],to_insert[15]))
        self.db.commit()

    def get_merge_info(self, date, string = None):
        '''
        Get the data required to print labels with merge
        @param Date after which we want the data
        @param Search string. Default = None
        '''
        DEBUG(date)
        if string is None:
            self.cur.execute("SELECT  asset_id, test_date, next_date \
                FROM assets WHERE test_date >= %s ORDER BY asset_id", (date,))
        else:
            string = '%' + string + '%'
            self.cur.execute("SELECT  asset_id, test_date, next_date \
                FROM assets WHERE test_date >= %s AND asset_id LIKE %s ORDER BY asset_id", \
                (date, string))
        result = self.cur.fetchall()
        return result


    def create_tables(self):
        return

if __name__ == '__main__':
    db = Database()
