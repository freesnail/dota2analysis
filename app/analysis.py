#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import dota2api

account_file = open('/home/jie/py/dota2api/account.txt', 'r')
api = dota2api.Initialise("0FC7F27CF84F15C2492359A7D52C10BC")

HERO_ID = 1
WIN = 0
LOSE = 0

def get_player_camp (slot):
    if slot in range (0, 5):
        return "Radiant"
    else:
        return "Dire"

def process_match (result, account):
    global WIN
    global LOSE
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
        print ("win %d lose %d win rate %f" % (WIN, LOSE, rate))


while True:
    line = account_file.readline()
    if not line:
        break
    else:
        print ("processing account: %s" % line)
        account = int(line)
        result = api.get_match_history(account_id = account, hero_id = HERO_ID, start_at_match_id = 3017815676)
        if int (result["num_results"]) > 0:
            process_match(result, account)


account_file.close()
    
