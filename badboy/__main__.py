#!/usr/bin/env python3

from argparse import ArgumentParser
from .badboy import badboy_terminal, connect
from .gui import Application
import tkinter as tk

def parse_args():
    parser = ArgumentParser(description=
        "Finds any horrific subreddits that a user might be a member of. Providing no arguments starts badboy in a gui mode.")
    parser.add_argument('user', nargs='?', help=
        "User's name")
    parser.add_argument('depth',nargs='?', type=int, default=500, help=
        "How far back to look in the user's submission and comment history. Defaults to 500.")
    parser.add_argument('top',nargs='?', type=int, default=3, help=
        "Number of highly upvoted comments to display. Defaults to 3.")
    opts = parser.parse_args()
    return opts

def main():
    opts = parse_args()
    if opts.user:
        badboy_terminal( connect(), opts.user, opts.depth, opts.top )
    else:
        Application( tk.Tk() ).mainloop()

if __name__ == "__main__":
    main()

