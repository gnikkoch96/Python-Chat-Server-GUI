import socket
import threading
from tools import Tools

# run this server first before running the client application

# server configurations
HEADER = 64  # contains the length of the actual message
PORT = 49951  # this is the port that the server will listen to for clients
SERVER_IP = socket.gethostbyname(socket.gethostname())  # gets the local ipv4 address
ADDR = (SERVER_IP, PORT)  # represents the server address
FORMAT = 'utf-8'  # used to encode messages to bytes and used for decoding back to string
DISCONNECT_MESSAGE = "DISCONNECT_ME"
DISCONNECT_SUCCESS = "DISCONNECT_SUCCESS"
GET_USERNAME_MESSAGE = "GET_USERNAME"

# create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen(100)  # configure server to listen to at most 100 connections
print(f"[LISTENING] Server is listening on {SERVER_IP}")

# holds client sockets
list_of_clients = []


def client_thread(conn, addr):
    # sends message to incoming user
    # todo: make this better
    welcome_msg, welcome_msg_len = Tools.format_msg_send("[SERVER] Welcome to the chatroom! Please be respectful =]",
                                                         HEADER, FORMAT)
    conn.send(welcome_msg_len)
    conn.send(welcome_msg)

    user_connected = True
    while user_connected:
        try:
            msg_len_info = conn.recv(HEADER).decode(FORMAT)
            if msg_len_info:  # checks to see if message is null
                msg_len = int(float(msg_len_info))
                msg = conn.recv(msg_len).decode(FORMAT)

                if msg == DISCONNECT_MESSAGE:
                    # disconnect user
                    user_connected = False

                    # grabs the username
                    get_user_msg, get_user_msg_len = Tools.format_msg_send(GET_USERNAME_MESSAGE, HEADER, FORMAT)
                    conn.send(get_user_msg_len)
                    conn.send(get_user_msg)
                    username_len_info = conn.recv(HEADER).decode(FORMAT)
                    if username_len_info:  # checks to see if message is null
                        username_len = int(float(username_len_info))
                        username = conn.recv(username_len).decode(FORMAT)

                        # notify all users that this user has disconnected
                        dc_msg = f"[DISCONNECT] {username} disconnected from server"
                        broadcast_user_message(dc_msg, conn)
                else:
                    broadcast_user_message(msg, conn)
                    print(f"{addr} {msg}")

        except ConnectionResetError:
            user_connected = False
            print(f"[DISCONNECT] {addr} disconnected from server")

# broadcasts the message to all users except for the one sending it
def broadcast_user_message(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                msg, msg_len = Tools.format_msg_send(message, HEADER, FORMAT)
                clients.send(msg_len)
                clients.send(msg)
            except:
                clients.close()


# main
while True:
    print("[WAITING] server is waiting for new users...")

    conn, addr = server.accept()  # conn - socket obj (user) and addr - ip addr of user (note: blocks)

    list_of_clients.append(conn)
    print(f"[NEW CONNECTION] {addr} connected.")

    user_thread = threading.Thread(target=client_thread, args=(conn, addr))
    user_thread.start()

    print(F"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
