from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
sys.path.append(os.path.abspath('..'))

from base.cluster import Cluster
from base.database import Database

class Node(object):
    def __init__(self, conf):
        self.ip = conf.get('ip', '127.0.0.1')
        self.ports = {'data_port': int(conf.get('data_port')), 'node_port': int(conf.get('node_port'))}
        self.ips = conf.get('ips')
        self.db = None
        try:
            self.database = Database(
                username=conf.get('dbusername'),
                password=conf.get('dbpassword'),
                host='127.0.0.1',
                port=int(conf.get('dbport')),
                dbname=conf.get('dbname'),
                dbtype=conf.get('dbtype'))
        except Exception as err:
            print(err)
            import traceback
            print(traceback.format_exc())

    def status(self):
        resd = {}
        resd['node'] = self.is_alive()
        resd['db'] = self.database.is_alive()
        print(resd)
        return resd

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
    node = Node('../dbsync.conf')
    print(node.ips)
    print(node.db.exec('show tables;'))
