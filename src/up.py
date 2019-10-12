import socket

HOST = '192.168.56.101'
PORT = 9999

udp_server_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_server_sock.bind((HOST, PORT))

while True:
    msg, addr = udp_server_sock.recvfrom(1024)
    udp_server_sock.sendto(str(addr).encode('utf-8') + msg,addr)
