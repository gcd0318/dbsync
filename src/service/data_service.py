from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from base.cluster import Cluster
from base.config import Config
from base.database import Database
from base.node import Node
from base.server import Server

from client.data_client import DataClient

from service import TCPService

from const import SQL_REQ


class DataService(TCPService):
    def __init__(self, conf_fn='../dbsync.conf', log_level=logging.DEBUG):
        TCPService.__init__(self, 'data', conf_fn, log_level)

    def spread_sql(self, sql):
        print(sql)
        resd = self._threading_spread_sql(sql)

    def _threading_spread_sql(self, sql):
        threads = []
        resd = {}

        def runner(resd, ip):
            print(ip, sql)
            r = None
            if(self.node.ip != ip):
                try:
                    client = DataClient(ip, self.node.data_port, timeout=5)
                    r = client.send_msg(sql)
                except Exception as err:
                    print(err)
                    import traceback
                    print(traceback.format_exc())
                    r = None
            else:
                r = self.node.database.exec(sql)
            resd[ip] = r

        for ip in self.node.cluster.node_ips:
            _t = threading.Thread(target=runner, args=(resd, ip))
            _t.start()
            threads.append(_t)

        for _t in threads:
            _t.join()
        return resd

    def _answer(self, addr, msg):
        sql = msg.replace(SQL_REQ, '')
        print(msg, type(msg), len(msg))
        print('from', addr, 'sql to exec:', sql)
        res = self.spread_sql(sql)
        return str(res)

if '__main__' == __name__:
    import sys
    t = 's'
    if 1 < len(sys.argv):
        t = sys.argv[1]
    dbs = DataService()
    print('server side')
    dbs.start()
