from tools import Tools
import socket
import threading
import sys, traceback

# dearpygui related
CHAT_ROOM_ID = "Chat Room"
CHAT_BOX_ID = "Chat Box"
CHAT_INPT_BOX_ID = " Chat Input Box"
CHAT_INPT_ID = "Chat Input"
SEND_BTN_ID = "Send Button"
ONLINE_LST_ID = "Online List"

# client related
HEADER = 64
FORMAT = 'utf-8'
PORT = 49950  # has to match the server side PORT
DISCONNECT_MESSAGE = "DISCONNECT_ME"
CLIENT_IP = socket.gethostbyname(socket.gethostname())
CLIENT_ADDR = (CLIENT_IP, PORT)


# this is the client app
class ChatRoom:
    def __init__(self, dpg, username):
        # create client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(CLIENT_ADDR)  # connects to server

        self.dpg = dpg
        self.username = username
        self.create_chat_room_win()
        self.dpg.set_primary_window(CHAT_ROOM_ID, True)
        self.isRunning = True

        # gui thread (used to check if gui is still active)
        gui_thread = threading.Thread(target=self.update_gui)
        gui_thread.start()

        # create receiving thread (this thread will mainly be receiving messages)
        rcv_thread = threading.Thread(target=self.rcv_msg, daemon=True)
        rcv_thread.start()

    def update_gui(self):
        while self.isRunning:
            if not self.dpg.is_dearpygui_running():
               # todo: if the gui is closed by the user, then make sure to close everything (i.e. sockets, send the disconnect message, etc...)
               self.isRunning = False

    def rcv_msg(self):
        # receive any messages sent to it by the server
        while self.isRunning:
            msg_len_info = self.client.recv(HEADER).decode(FORMAT)
            if msg_len_info:
                try:
                    msg_len = int(float(msg_len_info))
                    msg = self.client.recv(msg_len).decode(FORMAT)

                    # update to gui (checks to see if the gui has been updated properly)
                    # todo: create a new input text in dpg and set the value of that with the incoming msg
                    self.dpg.set_value("Dum Box", msg)

                except ConnectionAbortedError:  # means something went wrong while closing the socket
                    break

                except:  # close the socket if any other error appears
                    print("Exception in user code:")
                    print("-" * 60)
                    traceback.print_exc(file=sys.stdout)
                    print("-" * 60)
                    self.client.close()
                    break

    def send(self):
        msg = self.username + ": " + self.dpg.get_value("Dum")
        self.dpg.set_value("Dum", "")

        user_msg = msg.encode(FORMAT)
        usr_msg_len_info = len(user_msg)
        usr_msg_len = str(usr_msg_len_info).encode(FORMAT)
        usr_msg_len += b' ' * (HEADER - len(usr_msg_len))  # pads the header
        self.client.send(usr_msg_len)
        self.client.send(user_msg)

    def create_chat_room_win(self):
        # Chat Room Window
        # todo: adjust the height and width of the chat room
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
                self.dpg.add_input_text(default_value="Connected Users")

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
                    # this will be a dummy field and will display the server's welcoming message
                    self.dpg.add_input_text(label="Chat Box",
                                            id="Dum Box")

                # Child 3: Input Box
                with self.dpg.child(id=CHAT_INPT_BOX_ID,
                                    height=self.dpg.get_viewport_height() * 0.25,
                                    width=self.dpg.get_viewport_width() * 0.75):
                    self.dpg.add_input_text(id=CHAT_INPT_ID)
                    self.dpg.add_button(label="Send",
                                        id=SEND_BTN_ID,
                                        callback=self.send)
