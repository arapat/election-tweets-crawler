
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json

#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

"""
Track keywords:

See http://seed.ucsd.edu/mediawiki/index.php/User:Julaiti_Alafate/Diary#Presidential_Election_2016.
"""

# Trace 1
trace1 = ['election 2016', '2016 presidential', 'election 16', 'presidential election', 'presidential candidate',
          'presidency 2016']
non_trace1 = ['ukraine', 'egypt', 'russia', 'afghanistan', 'syria', 'turkey', 'benghazi', 'iraq', 'colombia', 
              'ukrainian', 'indonesia', 'lebanon', 'lebanese', 'nuristani', 'yudhoyono', 'renamo', 'jakarta', 
              'poroshenko', 'abdullah', 'malawi', 'kenya', 'sunnis', 'tayyip', 'aoun', 'widodo', 'jokowi', 
              'prabowo', 'kurds', 'mec', 'apc', 'akufo', 'syria', 'assad', 'fattah', 'uganda', '2015', '2011']

# Trace 2
trace2a = ["joe biden", "lincoln chafee", "hillary clinton", "martin o malley", "bernie sanders", "jim webb"]
trace2b = ["biden", "chafee", "hillary", "clinton", "o malley", "sanders", "webb"]
trace2c = ["jeb bush", "ben carson", "chris christie", "ted cruz", "bob ehrlich", "mark everson", "carly fiorina",
           "jim gilmore", "lindsey graham", "mike huckabee", "bobby jindal", "john kasich", "pete king", 
           "george pataki", "rand paul", "rick perry", "marco rubio", "rick santorum", "donald trump", 
           "scott walker"]
trace2d = ["jeb", "bush", "christie", "cruz", "everson", "fiorina", "huckabee", "jindal", "kasich", "pataki",
           "rubio", "santorum", "trump" ]
trace2 = trace2a + trace2b + trace2c + trace2d
# Trace 3
trace3 = ["democratic nomination", "republican nomination", "democratic platform", "republican platform"]

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            raw_text = json.loads(data)['text']
        except:
            return True
        text = raw_text.lower()
        valid = False
        # Trace 2 and 3
        for trace in trace2 + trace3:
            keywords = trace.split()
            contains = [text.find(kw) >= 0 for kw in keywords]
            if all(contains):
                # print "Trace 2/3:", keywords
                valid = True
                break
        # Trace 1
        if not valid:
            missed = [text.find(keyword) < 0 for keyword in non_trace1]
            if all(missed):
                for trace in trace1:
                    keywords = trace.split()
                    contains = [text.find(kw) >= 0 for kw in keywords]
                    if all(contains):
                        # print "Trace 1", keywords
                        valid = True
                        break
        if valid:
            # print raw_text
            print data,
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    
    stream.filter(track=trace1 + trace2 + trace3)
