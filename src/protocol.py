# [TYPE] CMD

class Protocol(object):
    def __init__(self, msg):
        msg = msg.strip()
        if msg.startswith('[') and (']' in msg):
            self.type = msg[1:msg.find(']')]
            self.cmd = msg[msg.find(']') + 1:]