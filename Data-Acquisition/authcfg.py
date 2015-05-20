import ConfigParser

class AuthCfg(object):
   """This class reads the specified file using ConfigParser, and makes
   the twitter API/OAUTH keys available
   The config file should have the format:
       [consumer]
       key=xxx
       secret=xxx
       [access]
       token=xxx
       secret=xxx
   """
   def __init__(self, fileName):
      cp = ConfigParser.RawConfigParser()
      with open(fileName) as cfg:    
         cp.readfp(cfg)
         self.consumer_key = cp.get('consumer', 'key')
         self.consumer_secret = cp.get('consumer', 'secret')
         self.access_token = cp.get('access', 'token')
         self.access_token_secret = cp.get('access', 'secret')
