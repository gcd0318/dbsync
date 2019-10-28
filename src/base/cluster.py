from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys
sys.path.append(os.path.abspath('..'))

from config import Config

class Client(object):
    def __init__(self, server_ip):
        self.server = server_ip

class Cluster(object):
    def __init__(self, node_ips=[], conf_fn='../db.conf'):
        self.node_ips = node_ips
        if not node_ips:
            conf = Config(conf_fn).read_data()
            self.node_ips = conf.get('ips', '').split()

    '''
    def all_status(self, data):
        threads = []
        def runner(anode):
            data[anode.ip] = anode.status()

        for node in self.nodes:
            th = threading.Thread(target=runner, args=(node,))
            th.start()
            threads.append(th)
        for t in threads:
            t.join()
        return data
    '''

    def add_node(self, node_ip):
        self.node_ips.append(node_ip)

    def remove_node(self, node_ip):
        node_ips = []
        for ip in self.node_ips:
            if node_ip != ip:
                nodes.append(node_ip)
        self.node_ips = node_ips

#    def exec_sql(self, sql):
#        for node in nodes:
#            node.db.exec(sql)

if '__main__' == __name__:
    c = Cluster()
    print(c.node_ips)
    c.add_node('127.0.0.1')
    print(c.node_ips)
