import json
import os
import sys
import signal
import time

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
            time.sleep(.1)

def main():
    with RollingOutputFacet('foo', 2) as facet:
        ts = TweetSerializer(facet)
        ts.emit(('test 1','test 2'))
        ts.emit(('test 3',))
        ts.emit(('test 4','test 5'))

if __name__ == '__main__':
    main()
