#!/usr/bin/env python3

from praw import Reddit
from textwrap import wrap
from collections import deque
from .badlist import THE_LIST
from operator import itemgetter
from .credentials import setup_credentails, load_credentials

# TODO Real results, not just text (pie chart)
# TODO Reddit table format generator
# TODO Reddit quote generator

MAX_FAVS = 5
LEFT_DISPLACE = 15
HEADER_LENGTH = 70

def review( reddit_iter, depth, numb_top_entries=0 ):

    badRecord, generalRecord, best = {}, {}, deque(maxlen=numb_top_entries)

    for entry in reddit_iter.new(limit=depth):

        if numb_top_entries != 0 and (not best or entry.ups > best[0][0]):
            best.append((entry.ups, entry))
            best = deque( sorted(best, key=lambda x: x[0]), maxlen=numb_top_entries )

        sub_name = entry.subreddit.display_name
        generalRecord[sub_name] = generalRecord.get(sub_name, 0) + 1

        if sub_name.lower() in THE_LIST:
            badRecord[sub_name] = badRecord.get(sub_name, 0) + 1

    checked = sum([v for v in generalRecord.values()])

    return checked, badRecord, generalRecord, [pair[1] for pair in best]

def connect():
    creds = load_credentials()
    if not creds:
        creds = setup_credentails()
    reddit = Reddit(username=creds.user, password=creds.password,
                    client_secret=creds.secret, client_id=creds.client_id,
                    user_agent=creds.agent)
    reddit.read_only = True
    return reddit

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Terminal

def print_best_comments( best ):
    for comment in reversed(best):
        print( "Top Comment in " + comment.subreddit.display_name + \
            "(" + str(comment.ups) + "):\n" + '\n'.join(wrap(comment.body,HEADER_LENGTH)), end='\n\n')

def print_bad_subject( checked, record, title ):
    br = str(sum(record.values()))
    percent = '0%' if checked == 0 else str(int((sum(record.values())/checked)*100)) + "%"
    print( ( ("-" * LEFT_DISPLACE) + title + " (" + br + "/" + str(checked) + \
        ", " + percent + ")" ).ljust(HEADER_LENGTH, '-') )
    for pair in record.items():
        print(pair[0] + ": " + str(pair[1]))
    print()

def print_fav_subject( checked, record, title ):
    print( (("-" * LEFT_DISPLACE) + title + " (" + str(checked) + ")").ljust(HEADER_LENGTH, '-') )
    for pair in sorted(record.items(), key=itemgetter(1), reverse=True)[0:MAX_FAVS]:
        print(pair[0] + ": " + str(pair[1]))
    print()

def badboy_terminal(reddit, user, depth, top):

    checked, badRecord, generalRecord, best = review( reddit.redditor(user).comments, depth, top )

    print_bad_subject( checked, badRecord, "Bad Comments" )
    print_fav_subject( checked, generalRecord, "Favorite Places to Comment" )
    print_best_comments( best )

    checked, badRecord, generalRecord, best = review( reddit.redditor(user).submissions, depth )

    print_bad_subject( checked, badRecord, "Bad Submissions" )
    print_fav_subject( checked, generalRecord, "Favorite Subs to Submit to" )


