from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys
sys.path.append(os.path.abspath('..'))
import threading

from base.client import Client
from base.config import Config
from base.db import DB
from base.node import Node
from base.server import Server

from service import TCPService

class DBService(TCPService):
    def __init__(self, name='dbservice', conf_fn='../db.conf', log_level=logging.DEBUG):
        conf = Config(conf_fn).read_data()
        host = conf.get('ip', '127.0.0.1')
        self.port = int(conf.get('hb_port'))
        self.server = TCPService.__init__(self, 'db', host, self.port, log_level)
        self.node = Node(conf_fn)

