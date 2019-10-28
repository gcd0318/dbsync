from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import logging.handlers
import os
import sys
sys.path.append(os.path.abspath('..'))

import socket

class Client(object):
    def __init__(self, name, server_host, server_port, socket_type='tcp', buff_size=1024, timeout=None, log_level=logging.DEBUG):
        self.name = name
        self.server_addr = (server_host, server_port)
        self.buff_size = buff_size
        self.socket = None
        self.socket_type = socket_type
        self._connect(timeout)

        self.logger = logging.getLogger(name)
        fh = logging.handlers.TimedRotatingFileHandler(self.name + '.log', "D", 1, 10)
        fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s_%(lineno)d: [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(fh)
        self.logger.setLevel(log_level)
        self.logger.info('connected to ' + server_host + ' as a ' + socket_type + ' client')


    def _connect(self, timeout=None):
        if 'tcp' == self.socket_type:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket.connect(self.server_addr)
        elif 'udp' == self.socket_type:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        if timeout is not None:
            self.socket.settimeout(timeout)

    def send_msg(self, msg, default_resp=None):
        resp = str(default_resp)
        res = None
        if 'tcp' == self.socket_type:
            self.socket.send(msg.encode('utf-8'))
            res = self.socket.recv(self.buff_size)
        elif 'udp' == self.socket_type:
            self.socket.sendto(msg.encode('utf-8'), self.server_addr)
            resp, addr = self.socket.recvfrom(self.buff_size)
            res = {'resp': resp.decode('utf-8'), 'addr': addr}
        return res

    def keep_send(self, msgs=[], quit_code=''):
        resl = []
#        if ('tcp' == self.socket_type) and (not quit_code in msgs):
#            msgs.append(quit_code)
        for msg in msgs:
            resl.append(self.send_msg(str(msg)))
        return resl


    def close(self):
        if self.socket is not None:
            self.socket.close()
        self.socket = None

    def __del__(self):
        if self.socket is not None:
            self.close()


if '__main__' == __name__:
    import sys

    HOST = '192.168.56.101'
    PORT = 9999

    server_type = 'tcp'
    if 1 < len(sys.argv):
        server_type = sys.argv[1]
 
    c = Client(HOST, PORT)
    c.connect(server_type)
    l = [1, 2, 3, 4, 5]
    resl = c.keep_send(l)
    c.close()
    for i in range(0, len(l)):
        print(i, l[i], resl[i])
    for i in resl:
        print(i)
