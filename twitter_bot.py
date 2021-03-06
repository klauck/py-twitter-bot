#!/usr/bin/env python
# pylint: disable=C0103

"""Twitter Bot. Listens for mentions and replies to them."""

#
# IMPORTS
#

# Allow using print as a function with parenthesis: print()
from __future__ import print_function
# basic operating system interactions
import os
import sys
# import the code that connects to Twitter
from twython import Twython, TwythonError
# import all functions from tweet_text.py
from tweet_text import *
# import all functions from helper.py
from helper import *

import requests
import datetime

# Try to import the variables defined in credentials.py
# If that does not exist (e.g. on Heroku), fall back to environment variables
try:
    from credentials import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
except ImportError as error:
    print('Info: {e}'.format(e=error))
    print('Info: Cannot load credentials.py. Will use environment variables.')
    try:
        APP_KEY = os.environ['APP_KEY']
        APP_SECRET = os.environ['APP_SECRET']
        OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
        OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']
    except KeyError as error:
        print('Error: {e} not found in environment variables'.format(e=error))
        print('Error: Could not retrieve credentials from either credentials.py or environment variables. Make sure either is set.')
        # can't do anything without credentials, so quit
        sys.exit()


#
# BOT CODE
#

def setup():
    # Login to Twitter
    account = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # Check the supplied credentials, get some general info on the account
    # https://dev.twitter.com/rest/reference/get/account/verify_credentials
    info = account.verify_credentials(include_entities=False, skip_status=True, include_email=False)
    print('user:', info['screen_name'])
    print('tweet count:', info['statuses_count'])
    print('favourite count:', info['favourites_count'])
    print('friends count:', info['friends_count'])
    return account

def tweet(account):
    """check for mentions and answer, otherwise tweet idle tweet"""
    replied = False
    mentions = account.get_mentions_timeline()
    rate_limit_remaining = account.get_lastfunction_header('x-rate-limit-remaining')
    print('rate limit remaining', rate_limit_remaining)

    repositories = requests.get('https://api.github.com/users/klauck/repos').json()
    updated_repositories = []
    for repository in repositories:
        updated_at = datetime.datetime.strptime(repository['pushed_at'][:10], '%Y-%m-%d').date()
        if updated_at == (datetime.datetime.now() - datetime.timedelta(days=1)).date():
            updated_repositories.append(repository['full_name'])

    if len(updated_repositories) > 0:
        text = 'New commits for: %s' % (', '.join(updated_repositories))
        tweet = account.update_status(status=text)
        print('https://twitter.com/statuses/{id}'.format(id=tweet['id']))


if __name__ == "__main__":
    account = setup()
    tweet(account)
