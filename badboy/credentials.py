#!/usr/bin/env python3

import pickle
from collections import namedtuple

CRED_FILE = 'user_credentials'

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
        pickle.dump(creds, fh, protocol=pickle.HIGHEST_PROTOCOL)

    return creds

def load_credentials():
    try:
        with open(CRED_FILE, 'rb') as fh:
            creds = pickle.load(fh)
        if all(creds):
            return creds
    except:
        pass

    return None
