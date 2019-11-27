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


class Service(object):
    def __init__(self, conf_fn='../dbsync.conf'):
        conf = Config(conf_fn).read_data()
        self.node = Node(conf)


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
