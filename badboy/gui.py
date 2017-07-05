#!/usr/bin/env python3

import tkinter as tk
from .badboy import connect, review, DEFAULT_DEPTH, DEFAULT_TOP

class Application(tk.Frame):

    WIN_HEIGHT = 100
    WIN_WIDTH  = 300
    RESULTS_WIDTH = 500
    RESULTS_HEIGHT = 500

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.wm_title("badboy")
        self.master.resizable(width=False, height=False)
        self.master.minsize(width=Application.WIN_WIDTH, height=Application.WIN_HEIGHT)
        self.master.maxsize(width=Application.WIN_WIDTH, height=Application.WIN_HEIGHT)
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
            self.display_text_review()

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

    def display_text_review(self):
        w = tk.Toplevel(self)
        w.wm_title(self.user)
        w.minsize(width=Application.RESULTS_WIDTH, height=Application.RESULTS_HEIGHT)
        w.maxsize(width=Application.RESULTS_WIDTH, height=Application.RESULTS_HEIGHT)

        l = tk.Text(w, height=int(Application.RESULTS_WIDTH/10), width=int(Application.RESULTS_HEIGHT/6.25))
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


