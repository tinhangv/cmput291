import sqlite3 as sq
import pprint
conn = sq.connect("test.db")
c = conn.cursor()
c.execute(' PRAGMA foreign_keys=ON; ')
conn.commit()





if __name__ == '__main__':
    
    conn.close()