from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading


from client import TCPClient
from base.const import SQL_REQ


class DataClient(TCPClient):

    def __init__(self, ip, data_port, timeout=5):
        TCPClient.__init__(self, 'data_client', ip, data_port, timeout=timeout)

    def send_sql(self, sql):
        sql = SQL_REQ + sql.strip()
        if not(sql.endswith(';')):
            sql = sql + ';'
        return eval(self.send_msg(sql).decode('utf-8'))

if '__main__' == __name__:
    dc = DataClient('192.168.56.101', 8888)
    import time
    while True:
        print(dc.send_sql('show tables;'))
        time.sleep(1)
