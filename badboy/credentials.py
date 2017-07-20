#!/usr/bin/env python3

from pickle import dump, load, HIGHEST_PROTOCOL
from collections import namedtuple
from os.path import expanduser, join
from os import remove

CRED_FILE = join( expanduser('~'), '.badboy_credentials' )

RedditCredentials = namedtuple('RedditCredentials', 'user password secret client_id agent')

def get_credentials():
    creds = load_credentials()
    if not creds:
        creds = setup_credentials()
    if not creds:
        return None
    return creds

def setup_credentials():
    print("Reddit script credentials have not been setup.")
    print("Please consult the readme if you are unsure of what to do.")
    user      = input("Username: ")
    password  = input("Password: ")
    secret    = input("Secret: ")
    client_id = input("Client ID: ")
    agent     = 'badboy'

    creds = RedditCredentials(user, password, secret, client_id, agent)
    if not all(creds):
        return None

    with open(CRED_FILE, 'wb+') as fh:
        dump(creds, fh, protocol=HIGHEST_PROTOCOL)

    return creds

def load_credentials():
    try:
        with open(CRED_FILE, 'rb') as fh:
            creds = load(fh)
        if not all(creds):
            remove(CRED_FILE)
            return None
    except:
        print('Issue loading the credentials file.')
        return None

    return creds
