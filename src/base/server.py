import socket
import logging
import logging.handlers

class Server(object):
    def __init__(self, name, host, port, log_level=logging.DEBUG):
        self.addr = (host, port)
        self.name = name
        self.logger = logging.getLogger(name)
        fh = logging.handlers.TimedRotatingFileHandler(name + '.log', "D", 1, 10)
        fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s_%(lineno)d: [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(fh)
        self.logger.setLevel(log_level)

    def tcp_start(self, max_conn=10, buff_size=1024, quit_code=''):
        self._start('tcp', max_conn, buff_size, quit_code)

    def udp_start(self, max_conn=10, buff_size=1024, quit_code=''):
        self._start('udp', max_conn, buff_size, quit_code)

    def _start(self, socket_type='tcp', max_conn=10, buff_size=1024, quit_code=''):
        socket_type = socket_type.lower()
        self.logger.debug('starting ' + self.name + ' as a ' + socket_type)

        if 'tcp' == socket_type:
            server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_sock.bind(self.addr)
            server_sock.listen(max_conn)
            self.logger.debug('service started')
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

        elif 'udp' == socket_type:
            self.logger.debug('service started')
            server_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            server_sock.bind(self.addr)
            while True:
                msg, addr = server_sock.recvfrom(buff_size)
                server_sock.sendto(self.reply(addr, msg), addr)

    def reply(self, *req):
        self.logger.debug('REQ: ' + str(req))
        res = ''
        for i in req:
            res = res + ' ' + str(i)
        res = res.strip()
        self.logger.debug('RESP: ' + res)
        return res.encode('utf-8')


if '__main__' == __name__:
    import sys
    import time

    HOST = '192.168.56.101'
    PORT = 9999

    serv = Server(name='sample', host=HOST, port=PORT)
    server_type = 'tcp'
    if 1 < len(sys.argv):
        server_type = sys.argv[1]
    while True:
        try:
            serv.start(server_type)
        except Exception as err:
            print(err)
            import traceback
            serv.logger.error(traceback.format_exc())
            print('wait 5 seconds.....')
            time.sleep(5)
