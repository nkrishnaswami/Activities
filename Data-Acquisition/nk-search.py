import sys
import tweepy
import datetime
import urllib
import signal
import json
import os
import sys
import time

from authcfg import AuthCfg
from tweetserializer import TweetSerializer
import facet as Facet

# Parse auth info from ".tweepy" in my home directory.
cfg = AuthCfg(os.path.expanduser('~/.tweepy'))
auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)
# create the API object
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# URL encoded query from cmd line
q = urllib.quote_plus(sys.argv[1])

def getJson(tweets):
   """little generator to extract the _json member from an iterable
   collection of tweet objects.

   """
   for tweet in tweets:
      yield tweet._json

# My TweetSerialzer takes a facet object as its init input. This is a
# context manager responsible for cleaning up in the event of an
# interrupt and ensuring the files it manages are properly terminated
# and closed.
with Facet.UsernameFacet(api) as facet:
#with Facet.RollingOutputFacet("tweets-{0}.json", 5000) as facet:
   ts = TweetSerializer(facet)
   for page in tweepy.Cursor(api.search,q=q,count=100).pages(10):
      print "Got {0} tweets".format(len(page))
      ts.emit(getJson(page))
      time.sleep(.2) # hack to permit cancellation; remove after python3 port
