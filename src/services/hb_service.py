from server import Server
from base.node import Node

class HeartBeatServer(Server):
    def __init__(self, host, port, log_level=logging.DEBUG):
        Server.__init__(self, 'heartbeat', host, port, log_level)

    def start(self):
        self.udp_start()

node = Node()


hb_server = HeartBeatServer()
hb_server.start('udp')