import os.path
import sqlite3
import time


class sqlite:
    def __init__(self, db):
        # 初始化
        self.conn = sqlite3.connect(db)

    def get_sql(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        time.sleep(1)

    def sel_sql(self, sql):
        # print(sql)
        cur = self.conn.cursor()
        return cur.execute(sql)

    def close(self):
        self.conn.close()
