#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import config

import MySQLdb
from Singleton import Singleton
from Pool import Pool, Constructor
from MySQLdb.cursors import Cursor
from log import log

class Dao(Singleton):

    def __init__(self):
        try:
            self.pool = Pool(Constructor(MySQLdb.connect, host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWD, db=config.DB_NAME, port=config.DB_PORT, charset="utf8", init_command="set autocommit=0", connect_timeout=5))
        except Exception,e:
            log(e)
            log("Can't retrive connection pool")

    def query(self, stmt):

        _query_done = False

        try:
            conn = self.pool.get()
            cursor = conn.cursor()
            cursor.execute(stmt)
            result = cursor.fetchall()
            _query_done = True
        except AttributeError, e:
            log(e)
            log("Database connection interrupted")
            time.sleep(2)
            self.query(stmt)
        except Exception, e:
            log(e)
            log("Attempt retry", stmt)
            time.sleep(2)
            self.query(stmt)
        finally:
            if _query_done:
                self.pool.restore(conn)

        return result

    @classmethod
    def getInstance(cls):
        if cls._singleton is None:
            cls._singleton = super(Dao, cls).__new__(cls)
        return cls._singleton


if __name__ == "__main__":
    Dao = Dao()
    r = Dao.query("select * from `image_queue` limit 10")
    print r
