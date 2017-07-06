#!/usr/bin/env python3

from pickle import dump, load
from collections import namedtuple
from os.path import expanduser, join

CRED_FILE = join( expanduser('~'), '.badboy_credentials' )

RedditCredentails = namedtuple('RedditCredentails', 'user password secret client_id agent')

def setup_credentails():
    print("Reddit script credentials have not been setup.")
    print("Please consult the readme if you are unsure of what to do.")
    user      = input("Username: ")
    password  = input("Password: ")
    secret    = input("Secret: ")
    client_id = input("Client ID: ")
    agent     = 'badboy'

    creds = RedditCredentails(user, password, secret, client_id, agent)

    with open(CRED_FILE, 'wb+') as fh:
        dump(creds, fh, protocol=pickle.HIGHEST_PROTOCOL)

    return creds

def load_credentials():
    try:
        with open(CRED_FILE, 'rb') as fh:
            creds = load(fh)
        if all(creds):
            return creds
    except:
        pass

    return None
