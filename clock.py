"""Regularly tweet"""

# Allow running functions periodically
# http://apscheduler.readthedocs.io/en/3.3.1/
from apscheduler.schedulers.blocking import BlockingScheduler
from twitter_bot import setup, tweet
import sys

account = setup()

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour='0')
def regular_tweet():
    tweet(account)

try:
    print('Info: {name} running.'.format(name=sys.argv[0]))
    print('Info: Will tweet every day at 0:00. Stop with Ctrl+c')
    scheduler.start()
# a KeyboardInterrupt exception is generated when the user presses Ctrl+c
except KeyboardInterrupt:
    print('\nInfo: Shutting down. Bye!')