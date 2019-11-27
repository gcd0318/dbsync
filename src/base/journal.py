import time

from const import SEP

class Journal(object):
    def __init__(self, jf_path):
        self.jf_path = jf_path

    def to_journal(self, msg):
        with open(self.jf_path, 'a') as f:
            print(time.localtime(), SEP, msg, file=f)

    def replay(self):
        with open(self.jf_path, 'r') as f:
            line = f.readline()
            while line is not None:
                exec(line.split(SEP, 1))
