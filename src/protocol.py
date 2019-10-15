# [TYPE] CMD

class Protocol(object):
    def __init__(self, msg):
        self.type, self.cmd = None, None
        msg = msg.strip()
        if msg.startswith('[') and (']' in msg):
            self.type = msg[1:msg.find(']')].strip()
            self.cmd = msg[msg.find(']') + 1:].strip()
