
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os
import sys
import json
from subprocess import Popen
from subprocess import PIPE

COUNTER_INIT = 0
TRACK_FILE = 'track-mar03.txt'

#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

# Track
track = []

def read_track():
  with open(TRACK_FILE) as f:
    for w in f:
      track.append(w.strip())
  print len(track)
  print track


class StdOutListener(StreamListener):

    def __init__(self):
      self.filename = 'tweets'
      self.threshold = 4 * 1024 * 1024 * 1024
      self.counter = COUNTER_INIT
      self.bucketName = ''

    def on_data(self, data):
      if os.path.isfile(self.filename) and os.stat(self.filename).st_size >= self.threshold:
        self.counter = self.counter + 1
        filename = 'election%03d' % self.counter
        sys.stdout.write('uploading %s...\n' % (filename))
        sys.stdout.flush()
        command = "aws s3 cp %s s3://%s/data/%s" % (self.filename, self.bucketName, filename)
        process = Popen(command, shell=True, stdout=PIPE)
        process.wait()
        os.remove(self.filename)
        sys.stdout.write('upload done.\n')
        sys.stdout.flush()

      json.loads(data)
      with open(self.filename, 'a') as f:
        f.write(data)
      return True

    def on_error(self, status):
      print status


if __name__ == '__main__':

    read_track()

    #This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    while True:
      try:
        stream.filter(track=track)
      except Exception as e:
        print e
        pass

