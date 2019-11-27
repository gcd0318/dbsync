from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from client import UDPClient

from const import CHECK_REQ

class NodeClient(UDPClient):
    def __init__(self, ip, node_port, timeout=5, log_level=logging.DEBUG):
        UDPClient.__init__(self, 'nodeclient', ip, node_port, timeout=5)

    def get_status(self):
        return self.send_msg(CHECK_REQ)


if '__main__' == __name__:
    nc = NodeClient('192.168.56.101', 9999)
    import time
    while True:
        print(nc.get_status())
        time.sleep(1)
