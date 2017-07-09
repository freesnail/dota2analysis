from __future__ import division
import os, sys, signal
import time, threading
from multiprocessing.dummy import Pool as ThreadPool
import dota2api
import logging
import logging.config
import pymysql

DB = pymysql.connect("localhost","root","123456", "dota2")
cursor = DB.cursor()

sql = "truncate table matches_normal"
cursor.execute(sql)
sql = "truncate table matches_high"
cursor.execute(sql)
sql = "truncate table matches_veryhigh"
cursor.execute(sql)
sql = "truncate table games_normal"
cursor.execute(sql)
sql = "truncate table games_high"
cursor.execute(sql)
sql = "truncate table games_veryhigh"
cursor.execute(sql)

DB.commit()
cursor.close()
DB.close()
