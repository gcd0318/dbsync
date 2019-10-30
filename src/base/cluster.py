from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import socket
import re
import sys
sys.path.append(os.path.abspath('..'))

from base.config import Config

class Cluster(object):
    def __init__(self, node_ips=[], conf_fn='../dbsync.conf'):
        self.node_ips = node_ips
        if not node_ips:
            conf = Config(conf_fn).read_data()
            self.node_ips = conf.get('ips', '').split()
        self.ready = {}
        for ip in self.node_ips:
            self.ready[ip] = False

    def update_status(self, status_dict):
        for ip in status_dict:
            if ip not in self.node_ips:
                self.node_ips.append(ip)
            self.ready[ip] = status_dict[ip]

    '''
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
