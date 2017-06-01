#!/usr/bin/python3

import sys
import praw
import operator
import argparse
import credentials
from badlist import THE_LIST

def is_badboy(reddit, baduser, depth):
    checked, bad_rec, gen_rec, best = review( reddit.redditor(baduser).comments, depth )
    bad_print( checked, bad_rec, "Bad Comments" )
    fav_print( checked, gen_rec, "Favorite Places to Comment" )
    best_print( best )
    checked, bad_rec, gen_rec, best = review( reddit.redditor(baduser).submissions, depth )
    bad_print( checked, bad_rec, "Bad Submissions" )
    fav_print( checked, gen_rec, "Favorite Subs to Submit to" )

def review( reddit_iter, depth ):
    checked = 0
    bad_rec = {}
    gen_rec  = {}
    best = None
    for subject in reddit_iter.new(limit=depth):
        if not best or subject.ups > best.ups:
            best = subject
        checked += 1
        sub_name = subject.subreddit.display_name.lower()
        gen_rec[sub_name] = gen_rec.get(sub_name, 0) + 1
        if sub_name in THE_LIST:
            bad_rec[sub_name] = bad_rec.get(sub_name, 0) + 1
    return checked, bad_rec, gen_rec, best

def best_print( best ):
    print( "Best Comment in " + best.subreddit.display_name + "(" + str(best.ups) + "): " + best.body, end='\n\n')

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

def parse_args():
    parser = argparse.ArgumentParser(description="Finds any horrific subreddits that a user might be a member of.")
    parser.add_argument('user', help="User's name")
    parser.add_argument('depth',nargs='?',default=500, help="How far back to look in the user's submission and comment history. Defaults to 500.")
    opts = parser.parse_args()
    return opts.user, int(opts.depth)

def main():
    is_badboy( connect(), *parse_args() )

if __name__ == "__main__":
    main()

