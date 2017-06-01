#!/usr/bin/python3

import sys
import praw
import operator
import argparse
import credentials
from badlist import THE_LIST

CHECK_DEPTH = 1000

def is_badboy(reddit, baduser):
    checked, bad_rec, gen_rec = review( reddit.redditor(baduser).comments )
    bad_print( checked, bad_rec, "Bad Comments" )
    fav_print( checked, gen_rec, "Favorite Places to Comment" )
    checked, bad_rec, gen_rec = review( reddit.redditor(baduser).submissions )
    bad_print( checked, bad_rec, "Bad Submissions" )
    fav_print( checked, gen_rec, "Favorite Subs to Submit to" )

def review( reddit_iter ):
    checked = 0
    bad_rec = {}
    record  = {}
    for comment in reddit_iter.new(limit=CHECK_DEPTH):
        checked += 1
        sub_name = comment.subreddit.display_name.lower()
        record[sub_name] = record.get(sub_name, 0) + 1
        if sub_name in THE_LIST:
            bad_rec[sub_name] = bad_rec.get(sub_name, 0) + 1
    return checked, bad_rec, record

def bad_print( checked, record, title ):
    print( (("-" * 5) + title + " (" + str(len(record)) + "/" + str(checked) + ", " + str(len(record)//checked) + "%)").ljust(50, '-') )
    for pair in record.items():
        print(pair[0] + ": " + str(pair[1]))
    print('')

def fav_print( checked, record, title ):
    print( (("-" * 5) + title + " (" + str(checked) + ")").ljust(50, '-') )
    i = 0
    for pair in sorted(record.items(), key=operator.itemgetter(1),reverse=True):
        if i == 5: break
        print(pair[0] + ": " + str(pair[1]))
        i += 1
    print('')

def review_list( reddit ):
    for sub in THE_LIST:
        if reddit.subreddit(sub):
            print('hello')

def connect():
    reddit = praw.Reddit(client_id=credentials.CLIENT_ID, client_secret=credentials.SECRET,
                         password=credentials.PASSWORD,   user_agent=credentials.AGENT,
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

