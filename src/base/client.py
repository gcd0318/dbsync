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
    def __init__(self, name, server_host, server_port, buff_size=1024, timeout=None, log_level=logging.DEBUG):
        self.name = name
        self.server_addr = (server_host, server_port)
        self.buff_size = buff_size
        self.socket = None
        self.logger = logging.getLogger(name)
        fh = logging.handlers.TimedRotatingFileHandler(self.name + '.log', "D", 1, 10)
        fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s_%(lineno)d: [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(fh)
        self.logger.setLevel(log_level)


    def close(self):
        if self.socket is not None:
            self.socket.close()
        self.socket = None

    def __del__(self):
        if self.socket is not None:
            self.close()

class TCPClient(Client):
    def __init__(self, name, server_host, server_port, buff_size=1024, timeout=10, log_level=logging.DEBUG):
        Client.__init__(self, name, server_host, server_port, buff_size=1024, timeout=10, log_level=logging.DEBUG)
        try:
            self._connect(timeout)
            self.logger.info('connected to ' + server_host + ' as a tcp client')
        except Exception as err:
            print(err)
            import traceback
            print(traceback.format_exc())

            self.logger.info('connected to ' + server_host + ' failed')


    def _connect(self, timeout=None):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#        print('addr:', self.server_addr)
        self.socket.connect(self.server_addr)
        if timeout is not None:
            self.socket.settimeout(timeout)


    def send_msg(self, msg, default_resp=None):
        resp = str(default_resp)
        self.socket.send(msg.encode('utf-8'))
        res = self.socket.recv(self.buff_size)
        return res

    def keep_send(self, msgs=[], quit_code=''):
        resl = []
        for msg in msgs:
            resl.append(self.send_msg(str(msg)))
        return resl


class UDPClient(Client):
    def __init__(self, name, server_host, server_port, buff_size=1024, timeout=None, log_level=logging.DEBUG):
        Client.__init__(self, name, server_host, server_port, buff_size=1024, timeout=None, log_level=logging.DEBUG)
        self._connect(timeout)
        self.logger.info('connected to ' + server_host + ' as a udp client')

    def _connect(self, timeout=None):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        if timeout is not None:
            self.socket.settimeout(timeout)

    def send_msg(self, msg, default_resp=None):
        resp = str(default_resp)
        self.socket.sendto(msg.encode('utf-8'), self.server_addr)
        resp, addr = self.socket.recvfrom(self.buff_size)
        res = {'resp': resp.decode('utf-8'), 'addr': addr}
        return res


if '__main__' == __name__:
    import sys

    HOST = '192.168.56.101'
    PORT = 9999

    c = TCPClient('', HOST, PORT)
    l = [1, 2, 3, 4, 5]
    resl = c.keep_send(l)
    print(c.send_msg('test'))
    c.close()
    for i in range(0, len(l)):
        print(i, l[i], resl[i])
    for i in resl:
        print(i)
