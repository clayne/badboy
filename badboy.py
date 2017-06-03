#!/usr/bin/python3

from praw import Reddit
from operator import itemgetter
from argparse import ArgumentParser
from collections import deque
from badlist import THE_LIST
from credentials import *
import tkinter as tk

MAX_FAVS = 5

def review( reddit_iter, depth, numb_top_entries=0 ):

    checked, badRecord, generalRecord, best = 0, {}, {}, deque(maxlen=numb_top_entries)

    for entry in reddit_iter.new(limit=depth):

        if numb_top_entries != 0 and (not best or entry.ups > best[0][0]):
            best.append((entry.ups, entry))
            best = deque( sorted(best, key=lambda x: x[0]), maxlen=numb_top_entries )

        checked += 1
        sub_name = entry.subreddit.display_name
        generalRecord[sub_name] = generalRecord.get(sub_name, 0) + 1

        if sub_name.lower() in THE_LIST:
            badRecord[sub_name] = badRecord.get(sub_name, 0) + 1

    return checked, badRecord, generalRecord, [pair[1] for pair in best]

def connect():
    reddit = Reddit(client_id=CLIENT_ID, client_secret=SECRET, password=PASSWORD,
                    user_agent=AGENT, username=USER)
    reddit.read_only = True
    return reddit

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# GUI Main

class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.server = connect()
        self.createWidgets()

    def createWidgets(self):
        self.start = tk.Button(self)
        self.start["text"] = "Review"

        self.user = tk.Text(self.master, height=1, width=10)
        self.depth = tk.Text(self.master, height=1, width=10)
        self.top = tk.Text(self.master, height=1, width=10)

        self.start["command"] = lambda : self.review_user(self.get_user(), self.get_depth(), self.get_top())

        self.start.pack(side="bottom")
        self.user.pack(side="bottom")
        self.depth.pack(side="bottom")
        self.top.pack(side="bottom")

        self.QUIT = tk.Button(self, text="QUIT", command=self.master.destroy)
        self.QUIT.pack(side="bottom")

    def review_user(self, user, depth, top):
        self.totalComments, self.badCommmentSummary, \
        self.generalCommentSummary, self.bestComments = \
            review( self.server.redditor(user).comments, depth, top )
        self.totalSubs, self.badSubSummary, \
        self.generalSubSummary, _ = \
            review( self.server.redditor(user).submissions, depth )

    def get_user(self):
        self.user.get("1.0",tk.END)

    def get_depth(self):
        self.depth.get("1.0",tk.END)

    def get_top(self):
        self.top.get("1.0",tk.END)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Terminal Printing

def print_best_comments( best ):
    for comment in best:
        print( "Top Comment in " + comment.subreddit.display_name + \
            "(" + str(comment.ups) + "): " + comment.body, end='\n\n')

def print_bad_subject( checked, record, title ):
    br = str(sum(record.values()))
    percent = '0%' if checked == 0 else str(sum(record.values())//checked) + "%"
    print( ( ("-" * 5) + title + " (" + br + "/" + str(checked) + \
        ", " + percent + ")" ).ljust(50, '-') )
    for pair in record.items():
        print(pair[0] + ": " + str(pair[1]))
    print()

def print_fav_subject( checked, record, title ):
    print( (("-" * 5) + title + " (" + str(checked) + ")").ljust(50, '-') )
    for pair in sorted(record.items(), key=itemgetter(1),reverse=True)[0:MAX_FAVS]:
        print(pair[0] + ": " + str(pair[1]))
    print()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Terminal Main

def badboy_terminal(reddit, user, depth, top):

    checked, badRecord, generalRecord, best = review( reddit.redditor(user).comments, depth, top )

    print_bad_subject( checked, badRecord, "Bad Comments" )
    print_fav_subject( checked, generalRecord, "Favorite Places to Comment" )
    print_best_comments( best )

    checked, badRecord, generalRecord, best = review( reddit.redditor(user).submissions, depth )

    print_bad_subject( checked, badRecord, "Bad Submissions" )
    print_fav_subject( checked, generalRecord, "Favorite Subs to Submit to" )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Arg Parse

def parse_args():
    parser = ArgumentParser(description=
        "Finds any horrific subreddits that a user might be a member of.")
    parser.add_argument('user', nargs='?', help=
        "User's name")
    parser.add_argument('depth',nargs='?',default=500, help=
        "How far back to look in the user's submission and comment history. Defaults to 500.")
    parser.add_argument('top',nargs='?',default=3, help=
        "Number of highly upvoted comments to display. Defaults to 3.")
    opts = parser.parse_args()
    return ( opts.user, int(opts.depth), int(opts.top) )

def main():
    opts = parse_args()
    if opts[0]:
        badboy_terminal( connect(), *opts )
    else:
        root = tk.Tk()
        app = Application(master=root)
        app.mainloop()

if __name__ == "__main__":
    main()


