from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from base.client import Client
from base.cluster import Cluster
from base.config import Config
from base.data import DB
from base.node import Node
from base.server import Server

from service import TCPService

class DBService(TCPService):
    def __init__(self, conf_fn='../db.conf', log_level=logging.DEBUG):
        TCPService.__init__(self, 'data', conf_fn, log_level)
        self.node = Node(conf_fn)
        self.cluster = Cluster()

    def spread_sql(self, sql):
        for ip in self.cluster.node_ips:
            client = Client(self.name, ip, self.port, socket_type='tcp', timeout=5)
            client.send_msg(sql)


if '__main__' == __name__:
    dbs = DBService()
    dbs.start_service()
    import time
    time.sleep(10)
    dbs.spread_sql('text')