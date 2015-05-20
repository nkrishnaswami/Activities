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
from tweetserializer import UsernameFacet
from tweetserializer import RollingOutputFacet
# Don't forget to install tweepy
# pip install tweepy

cfg = AuthCfg(os.path.expanduser('~/.tweepy'))

auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

q = urllib.quote_plus(sys.argv[1])  # URL encoded query

# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"

def getJson(tweets):
   for tweet in tweets:
      yield tweet._json
#with UsernameFacet() as facet:
with RollingOutputFacet("tweets-{0}.json", 1000) as facet:
   ts = TweetSerializer(facet)
   for page in tweepy.Cursor(api.search,q=q).pages(10): # 15 tweets at a time
      ts.emit(getJson(page))
