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
    def __init__(self, name='dbservice', conf_fn='../db.conf', log_level=logging.DEBUG):
        UDPService.__init__(self, name)
        self.node = Node(conf_fn)
        self.cluster = Cluster()

class TCPService(Service):
    def start_service(self):
        threading._start_new_thread(self.tcp_start, ())

def UDPService(Service):
    def start_service(self):
        threading._start_new_thread(self.udp_start, ())
