from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from base.client import TCPClient
from base.cluster import Cluster
from base.config import Config
from base.database import Database
from base.node import Node
from base.server import Server

from service import TCPService

REQ = '[SQL]'

class DBService(TCPService):
    def __init__(self, conf_fn='../dbsync.conf', log_level=logging.DEBUG):
        self.node = Node(Config(conf_fn).read_data())
        TCPService.__init__(self, 'data', self.node.ip, self.node.data_port, log_level)
        self.cluster = Cluster()

    def spread_sql(self, sql):
        self._threading_spread_sql(sql, self.cluster.node_ips)

    def _threading_spread_sql(self, sql, ips):
        threads = []
        resd = {}

        def runner(resd, ip):
            r = {}
            if(self.node.ip != ip):
                try:
                    client = TCPClient(self.name, ip, self.node.data_port, timeout=5)
                    r = {'resp': client.send_msg(sql)}
                except Exception as err:
                    print(err)
                    import traceback
                    print(traceback.format_exc())
                    r = {}
            else:
                r = {'resp': self.node.database.exec(sql)}
            resd[ip] = r.get('resp')

        for ip in ips:
            _t = threading.Thread(target=runner, args=(resd, ip))
            _t.start()
            threads.append(_t)

        for _t in threads:
            _t.join()
        return resd

    def _answer(self, msg):
        addr, sql = msg
        print('from', addr, 'sql to exec:', sql)
        return self.node.database.exec(sql)

if '__main__' == __name__:
    dbs = DBService()
    dbs.start_service()
    import time
    time.sleep(3)
    while True:
        print(dbs.spread_sql('show tables;'))
        time.sleep(1)
