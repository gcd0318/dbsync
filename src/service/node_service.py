from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from const import CHECK_REQ

from service import UDPService

from client.node_client import NodeClient


class NodeService(UDPService):
    def __init__(self, conf_fn='../dbsync.conf', log_level=logging.DEBUG):
        UDPService.__init__(self, 'node', conf_fn, log_level)

    def report_status(self):
        return str(self.node.status())

    def check_peer(self):
#        try:
#            res = self.send_msg(CHECK_REQ)
#        except Exception as err:
#            r = {}
#        return res
        return {**{self.node.ip: self.node.status()}, **self._threading_check(self.cluster.node_ips)} 

    def _threading_check(self):
        threads = []
        resd = {}

        def runner(resd, ip):
            r = {}
            try:
                r = NodeClient(ip, self.node.node_port).send_msg(CHECK_REQ)
            except Exception as err:
                print(err)
                import traceback
                print(traceback.format_exc())
#            print(r)
            resd[ip] = r.get('resp')

        for ip in self.cluster.node_ips:
            _t = threading.Thread(target=runner, args=(resd, ip))
            _t.start()
            threads.append(_t)

        for _t in threads:
            _t.join()
        return resd

    def _answer(self, addr, msg):
        res = ''
        print(addr, msg)
        if CHECK_REQ in msg:
            res = self.report_status()
#        print(res)
        return res

if '__main__' == __name__:
    hb_server = NodeService()
    hb_server.start()
