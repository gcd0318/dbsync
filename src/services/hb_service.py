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

from service import UDPService

REQ = 'CHECK STATUS FROM'

class HeartBeatServer(UDPService):
    def __init__(self, conf_fn='../db.conf', log_level=logging.DEBUG):
        UDPService.__init__(self, 'heartbeat', conf_fn, log_level)
        self.node = Node(conf_fn)
        self.cluster = Cluster()

    def start_service(self):
        super().start_service()
        while True:
            try:
                self.cluster.update_status(self.check_peer())
                print(self.cluster.ready)
            except Exception as err:
                print(err)
                import traceback
                print(traceback.format_exc())
            finally:
                import time
                time.sleep(5)

    def report_status(self):
        return str(self.node.status())

    def check_peer(self):
        resd = {self.node.ip: self.node.status()}
        for ip in self.cluster.node_ips:
            if(ip != self.node.ip):
                r = {}
                try:
                    client = Client(self.name, ip, self.port, socket_type='udp', timeout=5)
                    r = client.send_msg(REQ)
                except Exception as err:
                    r = {}
                resd[ip] = r.get('resp')
        return resd

    def _answer(self, msg):
        res = ''
        if REQ in msg:
            res = self.report_status()
        return res

if '__main__' == __name__:
    hb_server = HeartBeatServer()
    hb_server.start_service()
