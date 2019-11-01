from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from base.server import Server
from base.node import Node
from base.client import UDPClient
from base.cluster import Cluster
from base.config import Config
from base.const import CHECK_REQ

from service import UDPService


class NodeService(UDPService):
    def __init__(self, conf_fn='../dbsync.conf', log_level=logging.DEBUG):
        UDPService.__init__(self, 'node', conf_fn, log_level)

    def report_status(self):
        return str(self.node.status())

    def _answer(self, addr, msg):
        res = ''
        if CHECK_REQ in msg:
            res = self.report_status()
#        print(res)
        return res

if '__main__' == __name__:
    hb_server = NodeService()
    hb_server.start()
