import socket, re
from uuid import getnode as get_mac

HEADER = 64
PORT = 3074
SERVER = '192.168.1.98'
ADDR = (SERVER, PORT)
MAC = 'fc:f3:c3:7a:ec:ef' #(':'.join(re.findall('..', '%012x' % get_mac())))
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'

def send(msg):
    message=msg.encode(FORMAT)

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    send_length += b' '*(HEADER-len(send_length))

    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
send(MAC)

send('hello')
input()
send('asdfasdf')
input()
send(DISCONNECT_MESSAGE)

