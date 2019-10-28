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
from base.client import Client
from base.cluster import Cluster
from base.config import Config

REQ = 'CHECK STATUS FROM'

class HeartBeatServer(Server):
    def __init__(self, conf_fn='../db.conf', log_level=logging.DEBUG):
        conf = Config(conf_fn).read_data()
        host = conf.get('ip', '127.0.0.1')
        self.port = int(conf.get('hb_port'))
        Server.__init__(self, 'heartbeat', host, self.port, log_level)
        self.node = Node(conf_fn)
        self.cluster = Cluster()

    def start_service(self):
        threading._start_new_thread(self.udp_start, ())
        i = 0
        while True:
            try:
                self.check_peer()
            except Exception as err:
                print(err)
                i = i + 1
                print('no resp in 5 seconds')
            finally:
                import time
                time.sleep(5)
                print('wait 5')

    def report_status(self):
        res = 'BAD'
        if self.node.status():
            res = 'OK'
        return res

    def check_peer(self):
        res = {}
        for ip in self.cluster.node_ips:
            client = Client('heartbeat', ip, self.port, socket_type='udp', timeout=5)
            r = client.send_msg(REQ)
            print(r)
            res[ip] = (r['resp'] == 'OK') and ((ip, self.port) == r['addr'])
        print(res)
        return res

    def _answer(self, msg):
        res = ''
        if REQ in msg:
            res = self.report_status()
        return res

if '__main__' == __name__:
    hb_server = HeartBeatServer()
    hb_server.start_service()
