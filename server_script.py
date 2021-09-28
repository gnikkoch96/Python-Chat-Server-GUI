import socket
import threading

# run this server first before running the client application

# server configurations
HEADER = 64  # contains the length of the actual message
PORT = 49955  # this is the port that the server will listen to for clients
SERVER_IP = socket.gethostbyname(socket.gethostname())  # gets the local ipv4 address
ADDR = (SERVER_IP, PORT)  # represents the server address
FORMAT = 'utf-8'  # used to encode messages to bytes and used for decoding back to string
DISCONNECT_MESSAGE = "DISCONNECT_ME"

# create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen(100)  # configure server to listen to at most 100 connections
print(f"[LISTENING] Server is listening on {SERVER_IP}")

# holds client sockets
list_of_clients = []


def client_thread(conn, addr):
    # sends message to incoming user
    # conn.send("Welcome to the chatroom!")

    user_connected = True
    while user_connected:
        msg_len_info = conn.recv(HEADER).decode(FORMAT)
        if msg_len_info:  # checks to see if message is null
            msg_len = int(float(msg_len_info))
            msg = conn.recv(msg_len).decode(FORMAT)

            # todo: I'm thinking that we can check to see if the user has ended their gui then disconnect them if they did
            if msg == DISCONNECT_MESSAGE:
                # disconnect user
                user_connected = False

                # notify all users that this user has disconnected
                dc_msg = f"[DISCONNECT] {addr} disconnected from server"
                broadcast_user_message(dc_msg, conn)

                print(f"[DISCONNECT] {addr} disconnected from server")

            else:
                broadcast_user_message(msg, conn)


# broadcasts the message to all users except for the one sending it
def broadcast_user_message(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
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
