import socket
import server_script

# create client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_script.ADDR)


# todo: (delete this comment)
# this method will be called when the user hits the send button
def send(msg):
    user_msg = msg.encode(server_script.FORMAT)
    usr_msg_len_info = len(user_msg)
    usr_msg_len = str(usr_msg_len_info).encode(server_script.FORMAT)
    usr_msg_len += b' ' * (server_script.HEADER - len(usr_msg_len))  # pads the header
    client.send(usr_msg_len)
    client.send(user_msg)
