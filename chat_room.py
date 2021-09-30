import nameconfig
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
PORT = 49951  # has to match the server side PORT
DISCONNECT_MESSAGE = "DISCONNECT_ME"
GET_USERNAME_MESSAGE = "GET_USERNAME"
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
        # self.dpg.set_primary_window(CHAT_ROOM_ID, True)
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
                self.stop()

    def rcv_msg(self):
        # receive any messages sent to it by the server
        while self.isRunning:
            msg_len_info = self.client.recv(HEADER).decode(FORMAT)
            if msg_len_info:
                try:
                    msg_len = int(float(msg_len_info))
                    msg = self.client.recv(msg_len).decode(FORMAT)
                    if msg == GET_USERNAME_MESSAGE:
                        self.send_msg(self.username)
                    else:
                        # update to gui (checks to see if the gui has been updated properly)
                        # todo: create a new input text in dpg and set the value of that with the incoming msg
                        self.dpg.add_text(parent=CHAT_BOX_ID,
                                          default_value=msg,
                                          wrap=600)

                except ConnectionAbortedError:  # means something went wrong while closing the socket
                    break

                except:  # close the socket if any other error appears
                    print("Exception in user code:")
                    print("-" * 60)
                    traceback.print_exc(file=sys.stdout)
                    print("-" * 60)
                    self.client.close()
                    break

    # this method is used when we want to send the message from the input field
    def send(self):
        msg = f"{self.username} : {self.dpg.get_value(CHAT_INPT_ID)}"

        self.dpg.add_text(parent=CHAT_BOX_ID,
                          default_value=msg,
                          wrap=600)

        self.dpg.set_value(CHAT_INPT_ID, "")  # resets the input field

        user_msg, usr_msg_len = Tools.format_msg_send(msg, HEADER, FORMAT)
        self.client.send(usr_msg_len)
        self.client.send(user_msg)

    # this method is used when a specific message is sent like DISCONNECT_MESSAGE or GET_USERNAME_MESSAGE
    def send_msg(self, msg):
        user_msg, usr_msg_len = Tools.format_msg_send(msg, HEADER, FORMAT)
        self.client.send(usr_msg_len)
        self.client.send(user_msg)

    def exit_callback(self):
        self.isRunning = False

        # send dc message to the server
        dc_msg, dc_msg_len = Tools.format_msg_send(DISCONNECT_MESSAGE, HEADER, FORMAT)
        self.client.send(dc_msg_len)
        self.client.send(dc_msg)

        self.dpg.show_item("Name-Settings")
        self.dpg.delete_item(CHAT_ROOM_ID)

    def stop(self):
        self.isRunning = False
        self.client.close()
        exit(0)

    def create_chat_room_win(self):
        # Chat Room Window
        # todo: adjust the height and width of the chat room
        with self.dpg.window(label="Chat Room",
                             id=CHAT_ROOM_ID,
                             height=600,
                             width=1000):
            chat_rm_height = self.dpg.get_viewport_configuration(CHAT_ROOM_ID).get('height')
            chat_rm_width = self.dpg.get_viewport_configuration(CHAT_ROOM_ID).get('width')

            with self.dpg.menu_bar():
                self.dpg.add_menu_item(label="Exit Chat Room",
                                       callback=self.exit_callback)

            # Child 1: Online List (who is connected)
            with self.dpg.child(label="Online List",
                                id=ONLINE_LST_ID,
                                height=chat_rm_height,
                                width=chat_rm_width * 0.15):
                # todo: find a way to dynamically add input fields to display connected users
                self.dpg.add_input_text(default_value="Connected Users")

            self.dpg.add_same_line()
            with self.dpg.child(label="Chat Container",
                                height=chat_rm_height,
                                width=chat_rm_width * 0.85):
                # Child 2: Chat Box
                with self.dpg.child(label="Chat Box",
                                    id=CHAT_BOX_ID,
                                    height=chat_rm_height * 0.85,
                                    width=chat_rm_width * 0.85):
                    self.dpg.set_y_scroll(CHAT_BOX_ID, 1000)

                # Child 3: Input Box
                with self.dpg.child(id=CHAT_INPT_BOX_ID,
                                    height=chat_rm_height * 0.25,
                                    width=chat_rm_width * 0.85):
                    self.dpg.add_input_text(id=CHAT_INPT_ID)
                    self.dpg.add_button(label="Send",
                                        id=SEND_BTN_ID,
                                        callback=self.send)
