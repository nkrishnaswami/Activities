class RecordOutput(object):
    """This is a file-like object for writing JSON arrays to file.  Each
    string (record) sent to it by write() is written to the file it
    manages, prepended with a ",\n" if not the first record.  On
    open/close, it writes the JSON "[" and "]" needed to denote an
    array.

    """
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
