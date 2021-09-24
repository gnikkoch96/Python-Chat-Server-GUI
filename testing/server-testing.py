import socket
import threading

HEADER = 64  # shows the length of a message (in this case 64 bytes)
PORT = 49950  # using a dynamic port (49152-65535)
SERVER_IP = socket.gethostbyname(socket.gethostname())  # gets the ip address of this machine dynamically
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8' # used to convert string to bytes and vice versa
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)  # binds the ip to the port


# print(SERVER_IP)
# print(socket.gethostname())

def handle_client(conn, addr):
    # if the client disconnects, we also want the server to know that said user is disconnected

    print(f"f[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_len_info = conn.recv(HEADER).decode(FORMAT)  # decode message using the utf-8
        if msg_len_info:
            msg_len = int(float(msg_len_info))
            msg = conn.recv(msg_len).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECT] {addr} disconnected from server")

            print(f"[{addr}] {msg}")

    conn.close()


def start():
    server.listen()  # listening to connections
    print(f"[LISTENING] Server is listening on {SERVER_IP}")
    while True:
        conn, addr = server.accept()  # waits for connection, then stores it to conn and addr
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(F"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
