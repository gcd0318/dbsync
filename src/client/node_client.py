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

from services.service import UDPService

from base.const import CHECK_REQ

class NodeClient(UDPClient):
    def __init__(self, name, ip, node_port, timeout=5, log_level=logging.DEBUG):
        UDPClient.__init__(self, name, ip, node_port, timeout=5)

    def check_peer(self):
        try:
            res = self.send_msg(CHECK_REQ)
        except Exception as err:
            r = {}
        return res


        return {**{self.node.ip: self.node.status()}, **self._threading_check(self.cluster.node_ips)} 

    def _threading_check(self, ips):
        threads = []
        resd = {}

        def runner(resd, ip):
            r = {}
            try:
                r = self.send_msg(CHECK_REQ + self.node.ip)
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


if '__main__' == __name__:
    nc = NodeClient('nodeclient', '192.168.56.101', 9999)
    import time
    while True:
        print(nc.check_peer())
        time.sleep(1)
