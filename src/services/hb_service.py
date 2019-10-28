from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))

from base.server import Server
from base.node import Node

class HeartBeatServer(Server):
    def __init__(self, host, port, log_level=logging.DEBUG):
        Server.__init__(self, 'heartbeat', host, port, log_level)

    def start_service(self):
        self.udp_start()


if '__main__' == __name__:
    node = Node()

    hb_server = HeartBeatServer(host=node.ip, port=node.hb_port)
    hb_server.start_service()