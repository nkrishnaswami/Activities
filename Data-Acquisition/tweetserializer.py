import json
import os
import sys
import signal

class TweetSerializer(object):
    """There is not too much to this "TweetSerializer": if the facet is
    interested in a tweet, it emits it to the facet.  This seems like
    the right scope at which to block SIGINT, but the right functions
    to do it aren't available in Python 2.

    """

    def __init__(self, facet):
        self.facet = facet
    def emit(self, iterable):
        for item in iterable:
            if not self.facet.match(item):
                continue
            #Uncomment these for Python 3
            #signal.pthread_sigmask(signal.SIG_BLOCK, set(signal.SIGINT))
            self.facet.emit(item)
            #signal.pthread_sigmask(signal.SIG_UNBLOCK, set(signal.SIGINT))

def main():
    """This is a common idiom for tests.  main() runs some simple
    diagnostics of the class(es) defined in the file.

    """
    with RollingOutputFacet('foo', 2) as facet:
        ts = TweetSerializer(facet)
        ts.emit(('test 1','test 2'))
        ts.emit(('test 3',))
        ts.emit(('test 4','test 5'))
# and if this file is the script being invoked, we call main().
if __name__ == '__main__':
    main()
