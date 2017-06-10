#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import dota2api
import logging
import logging.config

logging.config.fileConfig("logging.config")
logger = logging.getLogger("main")

ACCOUNT_FILE = 0
HERO_ID_BASE = 0
HERO_ID_LAST = 113
WIN = 0
LOSE = 0
HERO_WINNING_RATE = {heroid: [0, 0] for heroid in range(HERO_ID_BASE, HERO_ID_LAST)}

api = dota2api.Initialise("0FC7F27CF84F15C2492359A7D52C10BC")

def get_player_camp (slot):
    if slot in range (0, 5):
        return "Radiant"
    else:
        return "Dire"

def process_player_match (result, account):
    global WIN
    global LOSE
    rate = 0
    for i in range (0, int(result["num_results"]) - 1):
        match = api.get_match_details(match_id = result["matches"][i]["match_id"])
        for i in range (0, 10):
            if int(match["players"][i]["account_id"]) == account:
                camp = get_player_camp (match["players"][i]["player_slot"])
                if camp == "Radiant" and match["radiant_win"]:
                    WIN += 1;
                elif camp == "Dire" and not match["radiant_win"]:
                    WIN += 1;
                else:
                    LOSE += 1;
                break;
        rate = float(WIN/(WIN + LOSE))
        logging.debug ("win %d lose %d win rate %f" % (WIN, LOSE, rate))
    return rate 

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

def get_hero_winning_rate (heroid):
    global WIN 
    global LOSE
    WIN = LOSE = 0
    while True:
        line = ACCOUNT_FILE.readline()
        if not line:
            break
        else:
            account = int(line)
            logging.debug ("processing account: %s" % line)
            result = api.get_match_history(account_id = account, hero_id = heroid, start_at_match_id = 3017815676)
            if int (result["num_results"]) > 0:
                rate = process_player_match(result, account)
    return rate


def main():

    if open_account_file() < 0:
        return -1

    for heroid in range(HERO_ID_BASE, HERO_ID_LAST):
        ACCOUNT_FILE.seek(0, os.SEEK_SET)
        logging.debug("start process hero id %d" % heroid)
        rate = get_hero_winning_rate(heroid)
        logging.info("hero id %d, winning rate %f" % (heroid, rate))
    return 0

if __name__ == "__main__":
    main()
    
