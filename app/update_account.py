#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import dota2api

account_file = open('/Users/Raspberrypi/py/dota2analysis/account.txt', 'w')
api = dota2api.Initialise("0FC7F27CF84F15C2492359A7D52C10BC")
count = 0

for uid in range (76400000, 76482431):
    if (count < 1000):
        try:
            result = api.get_match_history(account_id=uid, start_at_match_seq_num=3001179359, matches_requested=10)
        except dota2api.src.exceptions.APIError, e:
            pass
        else:
            print "valid user: ", uid
            account_file.write(str (uid) + '\n')
            count += 1
    else:
        break;

account_file.close()
    
#print result["matches"]
#match = api.get_match_details(match_id=3215007473)
#print match['radiant_win']
#match = api.get_match_details(match_id=3215606399)
#print match['radiant_win']

#result = api.get_top_live_games()
#print result
