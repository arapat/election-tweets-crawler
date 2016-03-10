import json
import os
import sys
from time import localtime, strftime

import boto3
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# a file in which we store the keywords for filtering the streaming result
TRACK_KEYWORDS_FILE_NAME = "track-mar03.txt"

# The streaming data will be saved locally until the the size of the local
# file exceeds MAXIMUM_FILE_SIZE. Then we uploaded the local file to AWS S3,
# rename it to REMOTE_FILE_NAME + sequential number, and delete the local file.
LOCAL_FILE_NAME = "tweets"
REMOTE_FILE_NAME = "tweets/stream"
REMOTE_FILE_NAME_STARTING_NUM = 0
MAXIMUM_FILE_SIZE = 4 * 1024 * 1024 * 1024  # local file won't exceed 4 GB
MAXIMUM_CACHE_SIZE = 1000

# Twitter API user credentials
TWITTER_ACCESS_TOKEN = ""
TWITTER_TOKEN_SECRET = ""
TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""

# Amazon S3 user credentials
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
AWS_REGION = ""
AWS_BUCKET_NAME = ""

# Track
track = []


def show_message(message):
    sys.stdout.write("[%s] " % strftime("%Y-%m-%d %H:%M:%S", localtime()))
    sys.stdout.write(message + "\n")
    sys.stdout.flush()


def read_track():
    with open(TRACK_KEYWORDS_FILE_NAME) as f:
        for w in f:
            track.append(w.strip())
    show_message("Number of keywords: %d" % len(track))
    show_message("All keywords: " + ", ".join(track))


class StdOutListener(StreamListener):
    def __init__(self, s3):
        self.s3 = s3
        self.counter = REMOTE_FILE_NAME_STARTING_NUM
        self.cache = []

    def on_data(self, data):
        if (os.path.isfile(LOCAL_FILE_NAME) and
                os.stat(LOCAL_FILE_NAME).st_size >= MAXIMUM_FILE_SIZE):
            self.counter = self.counter + 1
            key = "%s%03d" % (REMOTE_FILE_NAME, self.counter)
            show_message('Uploading %s...' % (key))
            self.s3.upload_file(LOCAL_FILE_NAME, AWS_BUCKET_NAME, key)
            os.remove(LOCAL_FILE_NAME)
            sys.stdout.write('Upload done.')
            sys.stdout.flush()

        self.cache.append(data)
        if len(data) >= MAXIMUM_CACHE_SIZE:
            with open(LOCAL_FILE_NAME, 'a') as f:
                f.write(''.join(self.cache))
            self.cache = []
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    # AWS authentication
    s3 = boto3.client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    # Twitter authentication
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET)
    listener = StdOutListener(s3)
    stream = Stream(auth, listener)

    read_track()
    while True:
        try:
            show_message('(Re)start streaming...')
            stream.filter(track=track)
        except Exception as e:
            # Keep the crawler running without being interupted by exceptions
            show_message("Exception (skipped):")
            show_message(str(e))
