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

for i in range(0, 130):
    sql = "INSERT INTO games_normal (hero_id) VALUE(%d)" % i
    cursor.execute(sql)
    sql = "INSERT INTO games_high (hero_id) VALUE(%d)" % i
    cursor.execute(sql)
    sql = "INSERT INTO games_veryhigh (hero_id) VALUE(%d)" % i
    cursor.execute(sql)
DB.commit()

for i in range(0, 130):
    sql = "UPDATE games_normal SET win = 0"
    cursor.execute(sql)
    sql = "UPDATE games_normal SET lose = 0"
    cursor.execute(sql)
    sql = "UPDATE games_high SET win = 0"
    cursor.execute(sql)
    sql = "UPDATE games_high SET lose = 0"
    cursor.execute(sql)
    sql = "UPDATE games_veryhigh SET win = 0"
    cursor.execute(sql)
    sql = "UPDATE games_veryhigh SET lose = 0"
    cursor.execute(sql)
DB.commit()

cursor.close()
DB.close()
