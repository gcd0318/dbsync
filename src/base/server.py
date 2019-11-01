import socket
import logging
import logging.handlers

class Server(object):
    def __init__(self, name, host, port, log_level=logging.DEBUG):
        self.addr = (host, port)
        self.name = name
#        self.host = host
#        self.port = port
        self.logger = logging.getLogger(name)
        fh = logging.handlers.TimedRotatingFileHandler(name + '.log', "D", 1, 10)
        fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s_%(lineno)d: [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(fh)
        self.logger.setLevel(log_level)

    def _answer(self, addr, msg):
        res = msg
        return res

    def reply(self, *req):
        self.logger.debug('REQ: ' + str(req))
        addr, msg = req
        res = self._answer(addr, msg.decode('utf-8'))
        print('res:', res, type(res))
        self.logger.debug('RESP: ' + res)
        return res.encode('utf-8')

class TCPServer(Server):
    def start(self, max_conn=10, buff_size=1024, quit_code=''):
        self.logger.debug('starting ' + self.name + ' as a tcp server')
        server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_sock.bind(self.addr)
        server_sock.listen(max_conn)
        self.logger.debug(self.name + 'service started: ' + str(self.addr))
        while True:
            client_sock, addr = server_sock.accept()
            self.logger.debug('connected from ' + str(addr))
            msg = client_sock.recv(buff_size).decode('utf-8')
            while (msg is not None) and (msg.lower() != quit_code):
                if msg is not None:
                    client_sock.send(self.reply(addr, msg))
                msg = client_sock.recv(buff_size).decode('utf-8')
            client_sock.close()
            self.logger.debug(str(addr) + ' quit')
        server_sock.close()

class UDPServer(Server):
    def start(self, max_conn=10, buff_size=1024, quit_code=''):
        self.logger.debug('starting ' + self.name + ' as a udp server')
        server_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server_sock.bind(self.addr)
        self.logger.debug(self.name + 'service started: ' + str(self.addr))
        while True:
            msg, addr = server_sock.recvfrom(buff_size)
            server_sock.sendto(self.reply(addr, msg), addr)


if '__main__' == __name__:
    import sys
    import time

    HOST = '192.168.56.101'
    PORT = 9999

    serv = TCPServer(name='sample', host=HOST, port=PORT)
    server_type = 'tcp'
    if 1 < len(sys.argv):
        server_type = sys.argv[1]
    while True:
        try:
            serv.start()
        except Exception as err:
            print(err)
            import traceback
            serv.logger.error(traceback.format_exc())
            print('wait 5 seconds.....')
            time.sleep(5)
