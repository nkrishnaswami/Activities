import json
import os
import sys
import signal

class RecordOutput(object):
    def __init__(self, file):
        self.file = file
        self.first = True
    def write(self, string):
        if not self.first:
            self.file.write(',\n')
        else:
            self.first = False
        self.file.write(string)
    def open(self):
        self.file.write('[\n')
    def close(self):
        self.file.write('\n]\n')
        self.file.close()
        self.file = None

class RollingOutput(object):
    def __init__(self, file_base, rec_limit):
        self.file = None
        self.file_base = file_base
        self.rec_limit = rec_limit
        self.file_count = 0
        self.rec_count = 0
    def close(self):
        if self.file: 
            self.file.close()
            self.file = None
    def open(self):
        self.file = RecordOutput(open(self.file_base.format(self.file_count), 'w'))
        self.file.open()
        self.file_count += 1

    def roll(self):
        if self.rec_count > 0 and self.rec_count >= self.rec_limit:
            self.close()
            self.rec_count = 0
        if not self.file:
            self.open()
    def write(self, string):
        self.roll()
        self.file.write(string)
        self.rec_count += 1
    def flush(self, *args, **kwargs): 
        self.file.flush(*args, **kwargs)
        self.roll()

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
import re
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
class TweetSerializer(object):
    def __init__(self, facet):
        self.facet = facet
    def emit(self, iterable):
        for item in iterable:
            if not self.facet.match(item):
                continue
            sig_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
            self.facet.emit(item)
            signal.signal(signal.SIGINT, sig_handler)

def main():
    with RollingOutputFacet('foo', 2) as facet:
        ts = TweetSerializer(facet)
        ts.emit(('test 1','test 2'))
        ts.emit(('test 3',))
        ts.emit(('test 4','test 5'))

if __name__ == '__main__':
    main()
