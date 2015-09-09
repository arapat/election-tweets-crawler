
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os
import json
from subprocess import Popen
from subprocess import PIPE

#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

# Trace
trace = ['donald trump', 'hillary clinton', 'bernie sanders', 'ted cruz', 'jeb bush', 'scott walker', 'ben carson', 'presidential candidate', 'joe biden', 'planned parenthood', 'marco rubio', 'bill clinton', 'rand paul', 'chris christie', 'birthright citizenship', 'presidential election', 'george bush', 'republican presidential', 'paul rand', 'sarah palin', 'john kasich', 'presidential candidates', 'running president', '2016 election', 'presidential campaign', 'gop candidates', 'super pac', 'presidential race', 'gop presidential', "martin o'malley", 'gop candidate', 'hilary clinton', 'republican party', 'elizabeth warren', 'presidential debate', 'next president', 'bush campaign', 'democratic party', 'president 2016', 'cruz 2016', 'democratic presidential', 'gop primary', 'democratic nomination', 'republican nomination'] \
    + ['trump', 'hillary', 'clinton', 'sanders', 'bernie', 'jeb', 'gop', 'biden', 'christie', 'republican', 'hillaryclinton', 'tedcruz', 'republicans', 'huckabee', 'berniesanders', 'democrats', 'jindal', 'jebbush', 'health', 'democrat', 'sensanders']

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self):
      self.threshold = 13100
      self.counter = 0

    def on_data(self, data):
        try:
            s = os.statvfs('/')
            if s.f_bavail <= self.threshold:
              self.counter = self.counter + 1
              filename = 'election%03d' % self.counter
              command = "aws s3 cp tweets s3://twitter-collect/data/%s" % filename
              process = Popen(command, shell=True, stdout=PIPE)
              process.wait()
              process = Popen("rm tweets", shell=True, stdout=PIPE)
              process.wait()
            json.loads(data)
            with open('tweets', 'a') as f:
              f.write(data)
        except:
            pass
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    while True:
      try:
        stream.filter(track=trace)
      except:
        pass

