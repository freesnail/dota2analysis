#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os, sys, signal
import time, threading
from multiprocessing.dummy import Pool as ThreadPool
import dota2api
import logging
import logging.config
import pymysql

#game level definition
ANY = 0
NORMAL = 1
HIGH = 2
VERY_HIGH = 3


logging.config.fileConfig("logging.config")
logger = logging.getLogger("main")

ACCOUNT_FILE = 0
HERO_ID_BASE = 0
HERO_ID_LAST = 115
#MATCHES_REQUESTED = 100
RECENT_VALID_MATCH_ID = 3017815676 
CAMP_RADIANT = 0
CAMP_DIRE = 1
HERO_WINNING_RATE = {heroid: [0, 0] for heroid in range(HERO_ID_BASE, HERO_ID_LAST)}
LEVEL = [NORMAL, HIGH, VERY_HIGH]
#THREAD_COUNT = 14

api = dota2api.Initialise("0FC7F27CF84F15C2492359A7D52C10BC")
lock = threading.Lock()
DB = pymysql.connect("localhost","root","123456", "dota2")
cursor = DB.cursor()

#watcher to response keybord interrupt
class Watcher():  
    def __init__(self):  
        self.child = os.fork()  
        if self.child == 0:  
            return  
        else:  
            self.watch()  
  
    def watch(self):  
        try:  
            os.wait()  
        except KeyboardInterrupt:  
            self.kill()  
        sys.exit()  
  
    def kill(self):  
        try:  
            os.kill(self.child, signal.SIGKILL)  
        except OSError:  
            pass  
def quit(signum, frame):
    logging.info("receive keyboard interrupt, quit")    
    sys.exit()

def get_player_camp (slot):
    if slot in range (0, 5):
        return CAMP_RADIANT
    else:
        return CAMP_DIRE

def process_hero_result(hero_id, hero_camp, radiant_win, level):
    global HERO_WINNING_RATE
    if radiant_win:
        if hero_camp == CAMP_RADIANT:
            HERO_WINNING_RATE[hero_id][0] += 1
        else: 
            HERO_WINNING_RATE[hero_id][1] += 1
    else:
        if hero_camp == CAMP_DIRE:
            HERO_WINNING_RATE[hero_id][0] += 1
        else: 
            HERO_WINNING_RATE[hero_id][1] += 1

def is_AI_match(match):
    if match["human_players"] < 10:
        return True
    else:
        return False

def match_processed(match_id):
    sql = "INSERT IGNORE INTO matches (match_id) VALUES (%d)" % (match_id)
    try:
        cursor.execute(sql)
        DB.commit()
    except:
        DB.rollback()

    return False

def process_matches (result, level):
    print (result["num_results"], level)
    for i in range (0, int(result["num_results"])):
        match_id = (int)(result["matches"][i]["match_id"])
        print (match_id)
        if not match_processed(match_id):
            match = api.get_match_details(match_id = match_id)
            if is_AI_match (match):
                continue
            if match:
                for i in range(0, 10):
                    hero_id = match["players"][i]["hero_id"]
                    camp = get_player_camp(match["players"][i]["player_slot"])
                    lock.acquire()
                    try:
                        process_hero_result (hero_id, camp, match["radiant_win"], level)
                    finally:
                        lock.release()
    return 0

def process_level_match (level):
    result = api.get_match_history (skill = level, matches_requested = 50)
    process_matches (result, level);
    logging.debug ("finished processing level: %d" % level)

def main():

    pool = ThreadPool()

    results = pool.map(process_level_match, LEVEL)

    pool.close() 
    pool.join()
    DB.close()
    #print (HERO_WINNING_RATE)
    return 0

if __name__ == "__main__":
    main()
    
