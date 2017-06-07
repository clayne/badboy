#!/usr/bin/env python3

from praw import Reddit
from operator import itemgetter
from argparse import ArgumentParser
from collections import deque
from badlist import THE_LIST
import tkinter as tk

try:
    from credentials import *
except ImportError:
    print("Please setup the credentails file.\n" + \
        "Consult the Readme for more information.")
    raise SystemExit

# TODO Ask for credientails and save them
# TODO Real results, not just text (pie chart)
# TODO Reddit table format generator
# TODO Reddit quote generator

MAX_FAVS = 5
WIN_HEIGHT = 100
WIN_WIDTH  = 300
DEFAULT_TOP = '3'
DEFAULT_DEPTH = '500'
RESULTS_WIDTH = 500
RESULTS_HEIGHT = 500

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
# GUI

class Application(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.wm_title("badboy")
        self.master.resizable(width=False, height=False)
        self.master.minsize(width=WIN_WIDTH, height=WIN_HEIGHT)
        self.master.maxsize(width=WIN_WIDTH, height=WIN_HEIGHT)
        self.server = connect()
        self.createWidgets()
        self.master.bind('<Return>', self.review_button)
        self.master.bind('<Escape>', self.close)

    def createWidgets(self):
        self.l_user  = tk.Label(self.master, text="User: ").grid(row=0, column=0, sticky='e')
        self.l_depth = tk.Label(self.master, text="Search Depth: ").grid(row=1, column=0, sticky='e', padx=(8,0))
        self.l_top   = tk.Label(self.master, text="Top Comments: ").grid(row=1, column=2, padx=(10,0), columnspan=2)

        self.w_user  = tk.Entry(self.master, width=22)
        self.w_depth = tk.Entry(self.master, width=3)
        self.w_top   = tk.Entry(self.master, width=3)

        self.w_user.grid(row=0, column=2, sticky='w', pady=5, columnspan=2)
        self.w_depth.grid(row=1, column=2, sticky='w', pady=5)
        self.w_top.grid(row=1, column=3, sticky='w', pady=5, padx=(112,0))

        self.w_review = tk.Button(self.master, text="Review",
            command=self.review_button).grid(row=2, column=1, columnspan=3, padx=(0,100))

        self.w_depth.insert(tk.END, DEFAULT_DEPTH)
        self.w_top.insert(tk.END, DEFAULT_TOP)

    def review_button(self, event=None):
        self.user = self.get_user()
        self.depth = self.get_depth()
        self.numb_top_comments = self.get_top()

        if ( self.review_user() ):
            self.display_review()

    def review_user(self):
        try:
            self.totalComments, self.badCommmentSummary, \
            self.generalCommentSummary, self.bestComments = \
            review( self.server.redditor(self.user).comments, self.depth, self.numb_top_comments )

            self.totalSubs, self.badSubSummary, \
            self.generalSubSummary, _ = \
            review( self.server.redditor(self.user).submissions, self.depth )

            return True
        except:
            print("Error Fetching User Data for '" + self.user + "'")
            return False

    def display_review(self):
        w = tk.Toplevel(self)
        w.wm_title(self.user)
        w.minsize(width=RESULTS_WIDTH, height=RESULTS_HEIGHT)
        w.maxsize(width=RESULTS_WIDTH, height=RESULTS_HEIGHT)

        l = tk.Text(w, height=(RESULTS_WIDTH//10), width=(RESULTS_HEIGHT//6.25))
        l.insert(tk.INSERT, 'This is a test!')
        l.pack()

    def close(self, event=None):
        raise SystemExit

    def get_user(self):
        return self.w_user.get().strip()

    def get_depth(self):
        try:
            return int(self.w_depth.get().strip())
        except:
            return 0

    def get_top(self):
        try:
            return int(self.w_top.get().strip())
        except:
            return 0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Terminal

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
        master = tk.Tk()
        app = Application(master)
        app.mainloop()

if __name__ == "__main__":
    main()


