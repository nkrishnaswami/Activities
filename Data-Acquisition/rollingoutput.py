from recordoutput import RecordOutput
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
