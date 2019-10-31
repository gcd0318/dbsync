from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from base.client import TCPClient

REQ = '[SQL]'

class DataClient(TCPClient):

    def __init__(self, name, ip, data_port, timeout=5):
        TCPClient.__init__(self, name, ip, data_port, timeout=timeout)

    def send_sql(self, sql):
        sql = REQ + sql.strip()
        if not(sql.endswith(';')):
            sql = sql + ';'
        print(sql)
        self.send_msg(sql)

if '__main__' == __name__:
    dc = DataClient('dataclient', '192.168.56.101', 8888)
    import time
    time.sleep(3)
    while True:
        print(dc.send_sql('show tables;'))
        time.sleep(1)
