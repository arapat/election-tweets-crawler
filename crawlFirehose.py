import json
import os
import sys
from time import localtime, strftime, sleep

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Twitter API user credentials
vault = json.load(open("credentials.json"))
TWITTER_ACCESS_TOKEN = vault["TWITTER_ACCESS_TOKEN"]
TWITTER_TOKEN_SECRET = vault["TWITTER_TOKEN_SECRET"]
TWITTER_CONSUMER_KEY = vault["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = vault["TWITTER_CONSUMER_SECRET"]


def show_message(message):
    sys.stdout.write("[%s] " % strftime("%Y-%m-%d %H:%M:%S", localtime()))
    sys.stdout.write(message + "\n")
    sys.stdout.flush()


class StdOutListener(StreamListener):
    def __init__(self):
        self._420 = 0
        self._okay_count = 0

    def on_data(self, data):
        print data
        self._okay_count += 1
        if self._okay_count >= 200:
            self._420 = 0
        return True

    def on_error(self, status_code):
        show_message("Error code: %d" % status_code)
        if status_code == 420:
            self._okay_count = 0
            self._420 = self._420 + 1
            show_message("Sleeping %d seconds before restart..." % (60 * self._420))
            sleep(60 * self._420)


if __name__ == '__main__':
    # Twitter authentication
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET)
    listener = StdOutListener()
    stream = Stream(auth, listener)

    while True:
        try:
            show_message('(Re)start streaming...')
            LOCATIONS = [-124.85, 24.39, -66.88, 49.38]
            stream.filter(locations=LOCATIONS)
        except Exception as e:
            # Keep the crawler running without being interupted by exceptions
            show_message("Exception: " + str(e))
