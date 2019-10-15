import socket
import logging
import logging.handlers

class Service(object):
    def __init__(self, name, host, port, log_level=logging.DEBUG):
        self.addr = (host, port)
        self.name = name
        self.logger = logging.getLogger(name)
        fh = logging.handlers.TimedRotatingFileHandler(name + '.log', "D", 1, 10)
        fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s_%(lineno)d: [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(fh)
        self.logger.setLevel(log_level)

    def start(self, socket_type='tcp', max_conn=10, buff_size=1024, quit_code='quit'):
        if 'tcp' == socket_type:
            server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_sock.bind(self.addr)
            server_sock.listen(max_conn)
            self.logger.debug(self.name + ' service started as a ' + socket_type)
            while True:
                client_sock, addr = server_sock.accept()
                self.logger.debug('connected from ' + str(addr))
                msg = ''
                while msg.lower() != quit_code:
                    msg = client_sock.recv(buff_size).decode('utf-8')
                    client_sock.send(self.reply(addr, msg).encode('utf-8'))
                client_sock.close()
                self.logger.debug(str(addr) + ' quit')

        elif 'udp' == socket_type:
            server_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.logger.debug(self.name + ' service started as a ' + socket_type)
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
        return res


if '__main__' == __name__:
    HOST = '192.168.56.101'
    PORT = 9999
    serv = Service(name='sample', host=HOST, port=PORT)
    import time
    while True:
        try:
            serv.start()
        except Exception as err:
            print(err)
            print('wait 5 seconds.....')
            time.sleep(5)
