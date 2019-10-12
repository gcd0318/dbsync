import socket

BUFSIZE=1024

HOST = '192.168.56.101'
PORT = 9999

udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

back_msg = ''

while 'quit' != back_msg:
    msg=input('msg: ').strip()
    if msg == 'quit':
        break
    udp_client_socket.sendto(msg.encode('utf-8'), (HOST, PORT))

    back_msg,addr = udp_client_socket.recvfrom(BUFSIZE)
    print(back_msg.decode('utf-8'))

udp_client_socket.close()
