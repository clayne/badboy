#!/usr/bin/python3

import argparse
import credentials
from badlist import THE_LIST
import praw
import sys

CHECK_DEPTH = 1000

def is_badboy(reddit, baduser):
    checked, record = find_bad_subs( reddit.redditor(baduser).comments )
    summary_print( checked, record, "Comments")
    checked, record = find_bad_subs( reddit.redditor(baduser).submissions )
    summary_print( checked, record, "Submissions")

def find_bad_subs( reddit_iter ):
    checked = 0
    record = {}
    for comment in reddit_iter.new(limit=CHECK_DEPTH):
        checked += 1
        sub_name = comment.subreddit.display_name.lower()
        if sub_name in THE_LIST:
            try:
                record[sub_name] += 1
            except:
                record[sub_name] = 1
    return checked, record

def summary_print( checked, record, name ): 
    print( (("-" * 5) + name + " (" + str(checked) + ")").ljust(30, '-') )
    for pair in record.items():
        print(pair[0] + ": " + str(pair[1]))

def review_list( reddit ):
    for sub in THE_LIST:
        if reddit.subreddit(sub):
            print('hello')

def connect():
    reddit = praw.Reddit(client_id=credentials.CLIENT_ID,
                         client_secret=credentials.SECRET,
                         password=credentials.PASSWORD,
                         user_agent=credentials.AGENT,
                         username=credentials.USER)
    reddit.read_only = True
    return reddit

def parse_arg():
    parser = argparse.ArgumentParser(description="Finds any horrific subreddits that a user might be a member of.")
    parser.add_argument('user', help="User's name")
    opts = parser.parse_args()
    return opts.user

def main():
    is_badboy( connect(), parse_arg() )
        
if __name__ == "__main__":
    main()

