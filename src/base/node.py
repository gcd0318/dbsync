from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
sys.path.append(os.path.abspath('..'))

from base.config import Config
from base.dbaccess import DB
#from base.cluster import Cluster
from base.server import Server
from base.client import Client

class Node(object):
    def __init__(self, conf_fn='../db.conf'):
        conf = Config(conf_fn).read_data()
        self.ip = conf.get('ip', '127.0.0.1')
        self.hb_port = int(conf.get('hb_port'))
        self.ips = conf.get('ips')
        self.db = None
        try:
            self.db = DB(
                username=conf.get('username'),
                password=conf.get('password'),
                host=self.ip,
                port=int(conf.get('port')),
                dbname=conf.get('dbname'),
                dbtype=conf.get('db'))
        except Exception as err:
            print(err)
            import traceback
            print(traceback.format_exc())

    def status(self):
        res = self.is_alive()
        return res

    def is_alive(self):
        return True

    def update_conf(self, option, value, section='node'):
        self.config.write_data(section, option, str(value))

    def add_peer(self, anode):
        self.ips.append(anode.ip)
        self.update_conf('cluster', 'ips', self.ips)

    def remove_peer(self, anode):
        ips = []
        for ip in self.ips:
            if ip != anode.ip:
                ips.append(ip)
        self.ips = ips
        self.update_conf('cluster', 'ips', self.ips)

    def join_cluster(self, cluster):
        pass

    def sync_data(self):
        pass

    def service(self):
        pass


if '__main__' == __name__:
    node = Node('../db.conf')
    print(node.ips)
    print(node.db.exec('show tables;'))
