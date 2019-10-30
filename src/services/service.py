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
from base.client import Client
from base.cluster import Cluster
from base.config import Config


def get_host_port(name, conf_fn):
    conf = Config(conf_fn).read_data()
    host = conf.get('ip', '127.0.0.1')
    port = int(conf.get(name + '_port'))
    return host, port

class TCPService(TCPServer):
    def __init__(self, name, conf_fn='../db.conf', log_level=logging.DEBUG):
        host, port = get_host_port(name, conf_fn)
        TCPServer.__init__(self, name, host, port, log_level)

    def start_service(self):
        threading._start_new_thread(self.start, ())

class UDPService(UDPServer):
    def __init__(self, name, conf_fn='../db.conf', log_level=logging.DEBUG):
        host, port = get_host_port(name, conf_fn)
        UDPServer.__init__(self, name, host, port, log_level)

    def start_service(self):
        threading._start_new_thread(self.start, ())
