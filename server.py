import socket, threading

HEADER = 64
PORT = 3074
SERVER = '192.168.1.98'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
ALLOWED_MAC = ('fc:f3:c3:7a:ec:ef',)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

def handle_client(conn, addr):
    print(f"\n[NEW CONNECTION] {addr} is being checked for a handshake\n")
    connected = True

    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg in ALLOWED_MAC:
            print(f"[HANDSHAKE] {addr} MAC ADDRESS is allowed")
            conn.send("Handshake was successful".encode(FORMAT))
        else:
            print(f"[HANDSHAKE] {addr} MAC ADDRESS is NOT allowed")
            conn.send("Handshake was NOT successful".encode(FORMAT))
            connected = False

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            if msg == DISCONNECT_MESSAGE:
                conn.send("Disconnecting...".encode(FORMAT))
                connected = False
    conn.close()


def start():
    server.listen()
    print(f"[LISTEN] Server is listening on address {ADDR}")
    print("[WAIT] Server is waiting for an allowed MAC ADRESS")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is running.....")
start()
