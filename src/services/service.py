from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from base.server import Server
from base.node import Node
from base.client import Client
from base.cluster import Cluster
from base.config import Config

REQ = 'CHECK STATUS FROM'

class Service(Server):
    def __init__(self, name, conf_fn='../db.conf', log_level=logging.DEBUG):
        self.conf = Config(conf_fn).read_data()
        host = self.conf.get('ip', '127.0.0.1')
        self.port = int(self.conf.get('hb_port'))
        self.server = Server.__init__(self, name, host, self.port, log_level)

class TCPService(Service):
    def start_service(self):
        threading._start_new_thread(self.tcp_start, ())

class UDPService(Service):
    def start_service(self):
        threading._start_new_thread(self.udp_start, ())
