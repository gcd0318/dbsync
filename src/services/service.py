from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from base.server import TCPServer, UDPServer
from base.node import Node
from base.config import Config
from base.client import Client
from base.cluster import Cluster
from base.config import Config


def get_host_port(name, conf_fn):
    conf = Config(conf_fn).read_data()
    host = conf.get('ip', '127.0.0.1')
    port = int(conf.get(name + '_port'))
    return host, port

class Service(object):
    def __init__(self, conf_fn='../dbsync.conf'):
        conf = Config(conf_fn).read_data()
        self.node = Node(conf)
        self.cluster = Cluster(conf)

class TCPService(Service, TCPServer):
    def __init__(self, name, conf_fn='../dbsync.conf', log_level=logging.DEBUG):
        Service.__init__(self, conf_fn)
        TCPServer.__init__(self, name, self.node.ip, self.node.ports.get(name + '_port'))

    def start_in_thread(self):
        threading._start_new_thread(self.start, ())

class UDPService(Service, UDPServer):
    def __init__(self, name, conf_fn='../dbsync.conf', log_level=logging.DEBUG):
        Service.__init__(self, conf_fn)
        UDPServer.__init__(self, name, self.node.ip, self.node.ports.get(name + '_port'))

    def start_in_thread(self):
        threading._start_new_thread(self.start, ())
