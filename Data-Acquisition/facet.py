import json
import re
from rollingoutput import RollingOutput
class RollingOutputFacet(object): 
        def __init__(self, file_base, rec_limit):
            self.out = RollingOutput(file_base, rec_limit)
        def match(self, item):
            return True
        def __enter__(self):
            self.out.open()
            return self
        def __exit__(self, exc_type, exc_value, traceback):
            self.out.close()
        def emit(self, item):
            json.dump(item, self.out)

class UsernameFacet(object):
    def __init__(self, filter = None):
        self.files = {}
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
            return self.filter.match(item['user']['id_str'])
        return True
    def emit(self, item):
        if item['user']['id'] not in self.files:
            self.files[item['user']['id']] = RollingOutput('user_' + item['user']['id_str'] + '-{0}.json', 6000)
        json.dump(item, self.files[item['user']['id']])
