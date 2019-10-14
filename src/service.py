import socket
import logging
import logging.handlers

class Service(object):
    def __init__(self, name, host, port, log_level=logging.DEBUG):
        self.host = host
        self.port = port
        self.logger = logging.getLogger(name)
        fh = logging.handlers.TimedRotatingFileHandler(name + '.log', "D", 1, 10)
        fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s_%(lineno)d: [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(fh)
        self.logger.setLevel(log_level)

    def start(self):
        udp_server_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_server_sock.bind((self.host, self.port))

        self.logger.debug('service started....')

        while True:
            req, addr = udp_server_sock.recvfrom(1024)
            self.logger.debug('[REQ]' + str(addr) + ': ' + req.decode('utf-8'))
            udp_server_sock.sendto(self._reply(addr, req).encode('utf-8'), addr)

    def _reply(self, *req):
        res = ''
        for i in req:
            res = res + ' ' + str(i)
        return res.strip()


if '__main__' == __name__:
    HOST = '192.168.56.101'
    PORT = 9999
    serv = Service(name='sample', host=HOST, port=PORT)
    serv.start()