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
