from tools import Tools
import socket

CHAT_ROOM_ID = "Chat Room"
CHAT_BOX_ID = "Chat Box"
CHAT_INPT_ID = "Chat Input"
ONLINE_LST_ID = "Online List"

# client related
HEADER = 64
FORMAT = 'utf-8'
PORT = 49955  # has to match the server side PORT
DISCONNECT_MESSAGE = "DISCONNECT_ME"
CLIENT_IP = socket.gethostbyname(socket.gethostname())
CLIENT_ADDR = (CLIENT_IP, PORT)


# this is the client app
class ChatRoom:

    def __init__(self, dpg, username):
        self.dpg = dpg

        # create client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(CLIENT_ADDR)

        self.username = username

        # Chat Room Window
        with self.dpg.window(label="Chat Room",
                             id=CHAT_ROOM_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width()):

            # Child 1: Online List (who is connected)
            with self.dpg.child(label="Online List",
                                id=ONLINE_LST_ID,
                                height=self.dpg.get_viewport_height(),
                                width=self.dpg.get_viewport_width() * 0.25):
                # todo: find a way to dynamically add input fields to display connected users
                self.dpg.add_input_text(label="Dummy User")

            self.dpg.add_same_line()

            with self.dpg.child(label="Chat Container",
                                height=self.dpg.get_viewport_height(),
                                width=self.dpg.get_viewport_width() * 0.75):
                # Child 2: Chat Box
                with self.dpg.child(label="Chat Box",
                                    id=CHAT_BOX_ID,
                                    height=self.dpg.get_viewport_height() * 0.75,
                                    width=self.dpg.get_viewport_width() * 0.75):
                    # todo: find a way to dynamically add input fields to display messages
                    self.dpg.add_input_text(label="Chat Box")

                # Child 3: Input Box
                with self.dpg.child(label="Chat Input",
                                    id=CHAT_INPT_ID,
                                    height=self.dpg.get_viewport_height() * 0.25,
                                    width=self.dpg.get_viewport_width() * 0.75):
                    self.dpg.add_input_text(label="Dummy Input Box",
                                            id="Dummy Input Box")
                    self.dpg.add_button(label="Send",
                                        callback=self.send(self.dpg.get_value("Dummy Input Box")))

    def send(self, msg):
        print(msg)
        user_msg = msg.encode(FORMAT)
        usr_msg_len_info = len(user_msg)
        usr_msg_len = str(usr_msg_len_info).encode(FORMAT)
        usr_msg_len += b' ' * (HEADER - len(usr_msg_len))  # pads the header
        self.client.send(usr_msg_len)
        self.client.send(user_msg)
