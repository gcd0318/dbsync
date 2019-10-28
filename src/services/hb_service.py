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
from base.cluster import Cluster

REQ = 'CHECK STATUS FROM'

class HeartBeatServer(Server):
    def __init__(self, conf_fn='../db.conf', log_level=logging.DEBUG):
        conf = Config(conf_fn).read_data()
        host = conf.get('ip', '127.0.0.1')
        port = int(conf.get('hb_port'))
        Server.__init__(self, 'heartbeat', host, port, log_level)
        self.node = Node(conf_fn)
        self.cluster = Cluster()

    def start_service(self):
        threading._start_new_thread(self.udp_start, ())
        while True:
            self.check_peer(self.cluster.node_ips)

    def report_status(self):
        res = 'OK'
        return res

    def check_peer(self):
        for ip in self.cluster.node_ips:


    def _answer(self, msg):
        res = ''
        if REQ in msg:
            res = self.report_status()
        return res

if '__main__' == __name__:
    hb_server = HeartBeatServer()
    hb_server.start_service()