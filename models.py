''' 
 Under TV - a television box for the internet citizen

 You may use any Under TV project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2012 Emilio Mariscal (emi420 [at] gmail.com)
 
 Module description:
 
    Data model
 
'''
import sqlite3

class Data:
    def __init__(self):
        self.conn = sqlite3.connect('data.sql3')
        curs = self.conn.cursor()
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='data';"
        data_table = curs.execute(cmd).fetchone()
        if data_table == None:
            self._syncdb()        
        
    def _syncdb(self):
        curs = self.conn.cursor()
        cmd = '''CREATE TABLE data (id INTEGER PRIMARY KEY, key TEXT, value TEXT);'''
        return curs.execute(cmd)

    def filter(self, key, value):
        curs = self.conn.cursor()
        cmd = "select value from data where key='%s' and value='%s'" % (key, value)
        result = curs.execute(cmd)
        return result.fetchall()
        
    def get(self, key):
        # FIXME CHECK
        curs = self.conn.cursor()
        cmd = "select value from data where key='%s'" % key
        result = curs.execute(cmd)
        return result.fetchall()

    def create(self, key, value):
        curs = self.conn.cursor()
        cmd = "insert into data (key, value) values ('%s,%s')" % (key, value)
        return curs.execute(cmd)

    def update(self, key, value):
        # FIXME CHECK
        curs = self.conn.cursor()
        cmd = "update data set value=? where key='%s'" % key
        return curs.execute(cmd)

    