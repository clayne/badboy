# badboy

badboy reviews the recent comments and submissions of a reddit user and reports on them. If the user is found to be active in racist/sexist (or w/e) subs then the info is reported. Favorite subreddits are also reported on along with submissions.

## Setup

The below is summary lifted from the [praw docs](https://praw.readthedocs.io/en/latest/getting_started/authentication.html).

1. Go [here](https://www.reddit.com/prefs/apps/) and register a script. You can use your own account or a new one, it doesn't matter. You can use a 'redirect URL' of `http://localhost:8080`.
2. Record the following information:

* client_id: The client ID is the 14 character string listed just under “personal use script” for the desired developed application
* client_secret: The client secret is the 27 character string listed adjacent to secret for the application.
* password: The password for the Reddit account used to register the script application.
* username: The username of the Reddit account used to register the script application.

3. Update and rename the '_credentails.py' file.

## Usage
```
usage: badboy.py [-h] [user] [depth] [top]

Finds any horrific subreddits that a user might be a member of.

positional arguments:
  user        User's name
  depth       How far back to look in the user's submission and comment
              history. Defaults to 500.
  top         Number of highly upvoted comments to display. Defaults to 3.

optional arguments:
  -h, --help  show this help message and exit
```
