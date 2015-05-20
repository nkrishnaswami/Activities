import ConfigParser

class AuthCfg(object):
   def __init__(self, fileName):
      cp = ConfigParser.RawConfigParser()
      with open(fileName) as cfg:    
         cp.readfp(cfg)
         self.consumer_key = cp.get('consumer', 'key')
         self.consumer_secret = cp.get('consumer', 'secret')
         self.access_token = cp.get('access', 'token')
         self.access_token_secret = cp.get('access', 'secret')