import socket
import threading

PORT = 49950  # using a dynamic port (49152-65535)
SERVER_IP = socket.gethostbyname(socket.gethostname())  # gets the ip address of this machine dynamically
ADDR = (SERVER_IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) # binds the ip to the port

# print(SERVER_IP)
# print(socket.gethostname())

def handle_client(conn, addr):
    pass

def start():
    server.listen() # listening to connections
    while True:
        conn, addr = server.accept()  # waits for connection, then stores it to conn and addr
        thread = threading.Thread(target=handle_client, args=(conn, addr))

print("[STARTING] server is starting...")
start()
