#!/usr/bin/python3

import credentials
from badlist import the_list
import praw
import sys

if len(sys.argv) != 2:
    print("Need username!")
    sys.exit() 
baduser = sys.argv[1]

reddit = praw.Reddit(client_id=credentials.CLIENT_ID,
                     client_secret=credentials.SECRET,
                     password=credentials.PASSWORD,
                     user_agent=credentials.AGENT,
                     username=credentials.USER)
reddit.read_only = True

record = {}
for comment in reddit.redditor(baduser).comments.new(limit=None):
    sub_name = comment.subreddit.display_name.lower()
    if sub_name in the_list:
        try:
            record[sub_name] += 1
        except:
            record[sub_name] = 1

for pair in record.items():
    print(pair[0] + ": " + str(pair[1]))

