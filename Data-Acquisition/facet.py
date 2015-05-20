import json
import re
from rollingoutput import RollingOutput
"""The big idea here is that a facet consumes tweets.  It has two main methods:
  * match(tweet) -> boolean: indicates that the facet is interested in the tweet.
  * emit(tweet) -> provides the tweet to the facet for processing.
Facets should be context manager (). They should be created as
    with MyFacet(args) as facet:
        ts = TweetSerializer(facet)
        ...
to ensure that the facet is able to clean up on leaving the block."""

class RollingOutputFacet(object): 
    """This facet consumes all tweets, and writes them as records to a
    rolling set of files."""
    def __init__(self, file_format, rec_limit):
        """`file_format` should be a format string with a single `{0}` for the
        rolled file number"""
        self.out = RollingOutput(file_format, rec_limit)
    def match(self, item):
        return True
    def emit(self, item):
        json.dump(item, self.out)
    def __enter__(self):
        self.out.open()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.out.close()

class UsernameCache(dict):
    def __init__(self, api):
        self.api=api
    def __missing__(self, key):
        name = self.api.get_user(user_id=key).screen_name
        self[key] = name
        return name;
   
class UsernameFacet(object):
    def __init__(self, api, filter = None):
        self.files = {}
        self.users = UsernameCache(api)
        if filter:
            self.filter = re.compile(filter)
        else:
            self.filter = None
    def __enter__(self):
        return self;
    def __exit__(self, exc_type, exc_value, traceback):
        for (key, val) in self.files.iteritems():
            val.close()
        self.files = {}
        
    def match(self, item):
        if self.filter:
            return self.filter.match(self.users[item['user']['id_str']])
        return True
    def emit(self, item):
        if item['user']['id'] not in self.files:
            self.files[item['user']['id']] = RollingOutput('user_' + self.users[item['user']['id_str']] + '-{0}.json', 6000)
        json.dump(item, self.files[item['user']['id']])
