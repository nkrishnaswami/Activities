import os
import sys
import tweepy
import urllib
import json
import time
import signal

class TweetSerializer:
   out = None
   first = True
   count = 0
   def start(self):
      self.count += 1
      fname = "tweets-"+str(self.count)+".json"
      self.out = open(fname,"w")
      self.out.write("[\n")
      self.first = True

   def end(self):
      if self.out is not None:
         self.out.write("\n]\n")
         self.out.close()
      self.out = None

   def write(self,tweet):
      if not self.first:
         self.out.write(",\n")
      self.first = False
      self.out.write(json.dumps(tweet._json).encode('utf8'))

from authcfg import AuthCfg
cfg = AuthCfg(os.path.expanduser('~/.tweepy'))
auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
q = urllib.quote_plus(sys.argv[1])  # URL encoded query

ts = TweetSerializer()
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   ts.close()
   exit(1)
for (count,page) in enumerate(tweepy.Cursor(api.search,q=q).pages(10)): # 15 tweets at a time
    print "Opening file",count
    ts.start()
    try:
        for tweet in page:
            ts.write(tweet)
            time.sleep(1)
    finally:
        ts.end()
