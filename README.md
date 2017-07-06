## badboy

badboy reviews the recent comments and submissions of a reddit user and reports on them. If the user is found to be active in racist/sexist (or w/e) subs then the info is reported. Favorite subreddits are also reported on along with submissions.

### Install

You can run badboy without installing it passing it into python with the '-m' flag from the root directory of the package.

```
python3 -m badboy [Arguments, none to start gui]
```

Install as you would any other python program. You shouldn't use `sudo` to install Ipsy unless you have reviewed the source code.

```
pip3 install --user .
```

### Config

Badboy stores all of the below information as serialzed text to your home directory.
The below is summary lifted from the [praw docs](https://praw.readthedocs.io/en/latest/getting_started/authentication.html).

1. Go [here](https://www.reddit.com/prefs/apps/) and register a script. You can use your own account or a new one, it doesn't matter. You can use a 'redirect URL' of `http://localhost:8080`.
2. Record the following information:

* client_id: The client ID is the 14 character string listed just under “personal use script” for the desired developed application
* client_secret: The client secret is the 27 character string listed adjacent to secret for the application.
* password: The password for the Reddit account used to register the script application.
* username: The username of the Reddit account used to register the script application.

3. Upon launching badboy for the first time you will be prompted for this information.

### Usage

After install, the easiest way to use badboy from the command line is simply `badboy username`

```
usage: badboy [-h] [user] [depth] [top]

Finds any horrific subreddits that a user might be a member of. Providing no
arguments starts badboy in a gui mode.

positional arguments:
  user        User's name
  depth       How far back to look in the user's submission and comment
              history. Defaults to 500.
  top         Number of highly upvoted comments to display. Defaults to 3.

optional arguments:
  -h, --help  show this help message and exit
```

### Example Output

```
badboy spez

-----Bad Comments (3/500, 0%)---------------------
The_Donald: 3

-----Favorite Places to Comment (500)-------------
announcements: 357
cscareerquestions: 47
modnews: 33
ModSupport: 17
technology: 13

Top Comment in announcements(12697): > However, why not allow a small 5 minute window to change the title? It shouldn't be long enough to blow up but may be long enough to help prevent a typo

Totally reasonable.

Top Comment in announcements(13843): On Reddit.

Top Comment in announcements(22207): Reddit search might work by then.

-----Bad Submissions (1/500, 0%)------------------
The_Donald: 1

-----Favorite Subs to Submit to (500)-------------
reddit.com: 447
announcements: 16
programming: 7
ModSupport: 4
nsfw: 4
```
