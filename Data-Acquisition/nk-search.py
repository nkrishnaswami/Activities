import sys
import tweepy
import datetime
import urllib
import signal
import json
import os
import sys
from authcfg import AuthCfg
from tweetserializer import TweetSerializer
import facet as Facet
# Don't forget to install tweepy
# pip install tweepy

cfg = AuthCfg(os.path.expanduser('~/.tweepy'))

auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# URL encoded query
q = urllib.quote_plus(sys.argv[1])

def getJson(tweets):
   for tweet in tweets:
      yield tweet._json
with Facet.UsernameFacet(api) as facet:
#with Facet.RollingOutputFacet("tweets-{0}.json", 5000) as facet:
   ts = TweetSerializer(facet)
   for page in tweepy.Cursor(api.search,q=q,count=100).pages(10):
      ts.emit(getJson(page))
