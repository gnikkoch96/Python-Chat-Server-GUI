import socket

HEADER = 64  # shows the length of a message (in this case 64 bytes)
PORT = 49950  # using a dynamic port (49152-65535)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER_IP = socket.gethostbyname(socket.gethostname())  # gets the ip address of this machine dynamically
ADDR = (SERVER_IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)  # encode the string to bytes (this will be decoded in the server side as long
    # as it uses the same format

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # pads the header
    client.send(send_length)
    client.send(message)


message = ' '
while message != DISCONNECT_MESSAGE:
    send(input("Message: "))