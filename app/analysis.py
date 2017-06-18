#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os, sys, signal
import time, threading
from multiprocessing.dummy import Pool as ThreadPool
import dota2api
import logging
import logging.config

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
ACCOUNT = []
#THREAD_COUNT = 14

api = dota2api.Initialise("0FC7F27CF84F15C2492359A7D52C10BC")
lock = threading.Lock()

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

def process_hero_result(hero_id, hero_camp, radiant_win):
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

def process_matches (result):
    print "match count: %d" % result["num_results"]
    for i in range (0, int(result["num_results"]) - 1):
        matchid = result["matches"][i]["match_id"] 
        match = api.get_match_details(match_id = matchid)
        if is_AI_match (match):
            continue
        if match:
            for i in range(0, 10):
                hero_id = match["players"][i]["hero_id"]
                camp = get_player_camp(match["players"][i]["player_slot"])
                lock.acquire()
                try:
                    process_hero_result (hero_id, camp, match["radiant_win"])
                finally:
                    lock.release()
    return 0

def open_account_file():
    global ACCOUNT_FILE
    try:
        ACCOUNT_FILE = open('/home/jie/py/dota2analysis/data/account.txt', 'r')
    except:
        try:
            ACCOUNT_FILE = open('/Users/Raspberrypi/py/dota2analysis/data/account.txt', 'r')
        except:
            logging.error("cannot find account file")    
            return -1
    return 0

def close_account_file(account_file):
    ACCOUNT_FILE.close()

def process_account_match(account):
    logging.debug ("processing account: %d" % account)
    result = api.get_match_history(account_id = account, skill = VERY_HIGH, start_at_match_id = RECENT_VALID_MATCH_ID, matches_requested = 50)
    #result = api.get_match_history(game_mode = 2, skill = VERY_HIGH, matches_requested = 1000)
    rate = process_matches(result)
    logging.debug ("finished processing account: %d" % account)

def main():
    global ACCOUNT
    account_num = 0

    Watcher()

    if open_account_file() < 0:
        return -1

#read account id 
    while True:
        line = ACCOUNT_FILE.readline()
        if not line:
            logging.info("%d accounts loaded" % account_num)
            break
        else:
            account_num += 1
            account = int(line)
            ACCOUNT.append(account)
    pool = ThreadPool()
    results = pool.map(process_account_match, ACCOUNT)
    pool.close() 
    pool.join()

    print HERO_WINNING_RATE
    close_account_file(ACCOUNT_FILE)

    return 0

if __name__ == "__main__":
    main()
    
