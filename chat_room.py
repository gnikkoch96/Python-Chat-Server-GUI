from tools import Tools
import socket
from playsound import playsound
import threading
import sys, traceback
import nameconfig

# dearpygui related
NEW_VIEWPORT_HEIGHT = 875
NEW_VIEWPORT_WIDTH = 1200
WORD_WRAP_CNT = 850
CHAT_ROOM_ID = "Chat Room"
CHAT_BOX_ID = "Chat Box"
CHAT_INPT_BOX_ID = " Chat Input Box"
CHAT_INPT_ID = "Chat Input"
SEND_BTN_ID = "Send Button"
ONLINE_LST_ID = "Online List"

# playsound module
SOUND_PATH = "resources/sounds/notification.wav"

# client related
HEADER = 64
FORMAT = 'utf-8'
PORT = 49951  # has to match the server side PORT
DISCONNECT_MESSAGE = "DISCONNECT_ME"
DISCONNECT_SUCCESS = "DISCONNECT_SUCCESS"
GET_USERNAME_MESSAGE = "GET_USERNAME"
CLIENT_IP = socket.gethostbyname(socket.gethostname())
CLIENT_ADDR = (CLIENT_IP, PORT)


class ChatRoom:
    def __init__(self, dpg, username):
        # create client socket and connect to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(CLIENT_ADDR)

        self.dpg = dpg
        self.username = username
        self.dpg.set_viewport_height(NEW_VIEWPORT_HEIGHT)
        self.dpg.set_viewport_width(NEW_VIEWPORT_WIDTH)
        self.create_chat_room_win()
        self.dpg.set_primary_window(CHAT_ROOM_ID, True)
        self.isRunning = True

        # thread to listen to key presses
        key_listener_thread = threading.Thread(target=self.listen_to_keys)
        key_listener_thread.start()

        # create receiving thread (this thread will mainly be receiving messages)
        rcv_thread = threading.Thread(target=self.rcv_msg)
        rcv_thread.start()

    def rcv_msg(self):
        while self.isRunning:
            if not self.dpg.is_dearpygui_running():
                # closes everything when user closes the client app
                self.isRunning = False
            else:
                msg_len_info = self.client.recv(HEADER).decode(FORMAT)
                if msg_len_info:
                    try:
                        msg_len = int(float(msg_len_info))
                        msg = self.client.recv(msg_len).decode(FORMAT)
                        if msg == GET_USERNAME_MESSAGE:
                            self.send_msg(str(self.username))
                        else:
                            # update to gui
                            self.dpg.add_text(parent=CHAT_BOX_ID,
                                              default_value=msg,
                                              wrap=WORD_WRAP_CNT)

                            playsound(SOUND_PATH)

                    except ConnectionAbortedError:  # means something went wrong while closing the socket
                        break

                    except:  # close the socket if any other error appears
                        print("Exception in user code:")
                        print("-" * 60)
                        traceback.print_exc(file=sys.stdout)
                        print("-" * 60)
                        break

        # closes the client's socket when the app is closed
        self.client.close()
        exit(0)

    def listen_to_keys(self):
        while self.isRunning:
            if self.dpg.is_key_pressed(self.dpg.mvKey_Return) and self.dpg.is_item_focused(CHAT_INPT_ID):
                if not Tools.isBlank(self.dpg.get_value(CHAT_INPT_ID)):
                    self.send()

                    # reassigns focus back to the chat input field
                    self.dpg.focus_item(CHAT_INPT_ID)

    def send(self):
        msg = f"{self.username} : {self.dpg.get_value(CHAT_INPT_ID)}"

        self.dpg.add_text(parent=CHAT_BOX_ID,
                          default_value=msg,
                          wrap=WORD_WRAP_CNT)

        # resets the input field
        self.dpg.set_value(CHAT_INPT_ID, "")

        self.send_msg(msg)

    def send_msg(self, msg):
        usr_msg, usr_msg_len = Tools.format_msg_send(msg, HEADER, FORMAT)
        self.client.send(usr_msg_len)
        self.client.send(usr_msg)

    def exit_callback(self):
        self.isRunning = False

        # send dc message to the server
        self.send_msg(DISCONNECT_MESSAGE)

        self.dpg.set_viewport_height(700)
        self.dpg.set_viewport_width(1100)

        # user returns to NameConfig gui
        self.dpg.delete_item(CHAT_ROOM_ID)
        nameconfig.NameConfig(self.dpg)

    # front-end (gui portion)
    def create_chat_room_win(self):
        # Chat Room Window
        with self.dpg.window(id=CHAT_ROOM_ID,
                             height=NEW_VIEWPORT_HEIGHT,
                             width=NEW_VIEWPORT_WIDTH):
            chat_rm_height = self.dpg.get_viewport_configuration(CHAT_ROOM_ID).get('height')
            chat_rm_width = self.dpg.get_viewport_configuration(CHAT_ROOM_ID).get('width')

            # Menu
            with self.dpg.menu_bar():
                self.dpg.add_menu_item(label="Exit",
                                       callback=self.exit_callback)

            # Child 1: Online List
            with self.dpg.child(label="Online List",
                                id=ONLINE_LST_ID,
                                height=chat_rm_height * 0.85,
                                width=chat_rm_width * 0.15):
                self.dpg.add_text(default_value="Connected Users")

            # Child 2: Chat Container
            self.dpg.add_same_line()
            with self.dpg.child(height=chat_rm_height * 0.85,
                                width=chat_rm_width * 0.80):
                child_container_height = chat_rm_height
                child_container_width = chat_rm_width * 0.95

                # Sub-Child 1: Chat Box
                with self.dpg.child(label="Chat Box",
                                    id=CHAT_BOX_ID,
                                    height=child_container_height * 0.70,
                                    width=child_container_width * 0.80):
                    self.dpg.set_y_scroll(CHAT_BOX_ID, 1000)

                # Sub-Child 2: Input Box
                Tools.add_padding(self.dpg, 0, 15, False)
                with self.dpg.child(id=CHAT_INPT_BOX_ID,
                                    height=child_container_height * 0.10,
                                    width=child_container_width * 0.80):
                    # Input Field
                    Tools.add_padding(self.dpg, 35, 15, True)
                    self.dpg.add_input_text(id=CHAT_INPT_ID,
                                            width=725)

                    # Send Button
                    self.dpg.add_same_line()
                    self.dpg.add_button(label="Send",
                                        id=SEND_BTN_ID,
                                        callback=self.send)
