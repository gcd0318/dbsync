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

from service import UDPService

REQ = '[CHECK]'

class HeartBeatServer(UDPService):
    def __init__(self, conf_fn='../dbsync.conf', log_level=logging.DEBUG):
        self.node = Node(conf_fn)
        UDPService.__init__(self, 'heartbeat', self.node.ip, self.node.heartbeat_port, log_level)
        self.cluster = Cluster()

    def start_service(self):
        super().start_service()
        while True:
            try:
                self.cluster.update_status(self.check_peer())
                print(self.cluster.ready)
            except Exception as err:
                pass
            finally:
                import time
                time.sleep(5)

    def report_status(self):
        return str(self.node.status())

    def check_peer(self):
        return {**{self.node.ip: self.node.status()}, **self._threading_check(self.cluster.node_ips)} 

    def _threading_check(self, ips):
        threads = []
        resd = {}

        def runner(resd, ip):
            r = {}
            try:
                client = UDPClient(self.name, ip, self.node.heartbeat_port, timeout=5)
                r = client.send_msg(REQ + self.node.ip)
            except Exception as err:
#                print(err)
#                import traceback
#                print(traceback.format_exc())
                r = {}
#            print(r)
            resd[ip] = r.get('resp')

        for ip in ips:
            _t = threading.Thread(target=runner, args=(resd, ip))
            _t.start()
            threads.append(_t)

        for _t in threads:
            _t.join()
        return resd

    def _answer(self, msg):
        res = ''
        if REQ in msg:
            res = self.report_status()
#        print(res)
        return res

if '__main__' == __name__:
    hb_server = HeartBeatServer()
    hb_server.start_service()