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

dic_sql_matches = {NORMAL:"matches_normal", HIGH:"matches_high", VERY_HIGH:"matches_veryhigh"}
dic_sql_games = {NORMAL:"games_normal", HIGH:"games_high", VERY_HIGH:"games_veryhigh"}

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
    if (radiant_win == True and hero_camp == CAMP_RADIANT) or (radiant_win == False and hero_camp == CAMP_DIRE):
        sql_update = "UPDATE %s SET win = win + 1 WHERE hero_id = %d" % (dic_sql_games[level], hero_id)
    else:
        sql_update = "UPDATE %s SET lose = lose + 1 WHERE hero_id = %d" % (dic_sql_games[level], hero_id)
    print (sql_update)
    lock.acquire()
    try:
        cursor.execute(sql_update)
        DB.commit()
        ret = True
    except:
        DB.rollback()
        ret = False
        logging.error ("Error happens while update hero_result")
    finally:
        lock.release()

    return ret

def is_AI_match(match):
    if match["human_players"] < 10:
        return True
    else:
        return False

def match_processed(match_id, level):
    ret = False
    sql_query = "SELECT * FROM %s WHERE match_id = '%d'" % (dic_sql_matches[level], match_id)
    lock.acquire()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchone()
        if result == None:
            ret = False
        else:
            ret = True
    except:
        print (sql_query)
        logging.error ("Error happens while query match_id: %d" % (match_id))
    finally:
        lock.release()

    return ret

def sql_insert_match(match_id, level):
    sql_insert = "INSERT INTO %s(match_id) VALUES(%d)" % (dic_sql_matches[level], match_id)
    lock.acquire()
    try:
        cursor.execute(sql_insert)
        DB.commit()
        ret = True
    except:
        DB.rollback()
        ret = False
        logging.error ("Error happens while insert match_id: %d" % (match_id))
    finally:
        lock.release()

    return ret

def process_game_result(match, level):
    ret = False
    for i in range(0, 10):
        hero_id = match["players"][i]["hero_id"]
        camp = get_player_camp(match["players"][i]["player_slot"])
        ret = process_hero_result (hero_id, camp, match["radiant_win"], level)
        if ret == False:
            break

    return ret

def process_matches (result, level):
    print (result["num_results"], level)
    ret = False
    for i in range (0, int(result["num_results"])):
        match_id = (int)(result["matches"][i]["match_id"])
        print (match_id)
        if (match_processed (match_id, level) == False):
            try:
                match = api.get_match_details(match_id = match_id)
            except:
                logging.warning ("Connection error while fetching match details, continue")
                continue
            if is_AI_match (match):
                continue
            if match:
                if (process_game_result(match, level)):
                    ret = sql_insert_match(match_id, level)
        else:
            logging.debug ("match %d is processed" % (match_id))
    return ret

def process_level_match (level):
    while (True):
        result = None
        try:
            result = api.get_match_history (skill = level, matches_requested = 100)
        except:
            logging.warning ("Connection error while fetching matches")
            time.sleep(1)
        finally:
            if (result != None and result["num_results"] > 0):
                process_matches (result, level)
            
        logging.debug ("finished processing level: %d" % level)
        time.sleep(5);
    return 0

def main():
    pool = ThreadPool()
    results = pool.map(process_level_match, LEVEL)
    pool.close() 
    pool.join()
    cursor.close()
    DB.close()
    return 0

if __name__ == "__main__":
    main()
    
