import socket

class Client(object):
    def __init__(self, server_host, server_port, buff_size=1024):
        self.server_addr = (server_host, server_port)
        self.buff_size = buff_size
        self.socket = None
        self.socket_type = None

    def connect(self, socket_type='tcp'):
        self.socket_type = socket_type.lower()
        if 'tcp' == socket_type:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket.connect(self.server_addr)
        elif 'udp' == socket_type:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def send_msg(self, msg):
        if 'tcp' == self.socket_type:
            self.socket.send(msg.encode('utf-8'))
            res = self.socket.recv(self.buff_size)
        elif 'udp' == self.socket_type:
            self.socket.sendto(msg.encode('utf-8'), self.server_addr)
            resp, addr = self.socket.recvfrom(self.buff_size)
            res = {'resp': resp, 'addr': addr}
        return res

    def keep_send(self, msgs=[]):
        resl = []
        if not 'quit' in msgs:
            msgs.append('quit')
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
    HOST = '192.168.56.101'
    PORT = 9999

    c = Client(HOST, PORT)
    c.connect('tcp')
    l = [1, 2, 3, 4, 5]
    resl = c.keep_send(l)
    c.close()
    for i in range(0, len(l)):
        print(i, l[i], resl[i])
    for i in resl:
        print(i)
