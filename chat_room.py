from tools import Tools
import socket
from playsound import playsound
import threading
import sys, traceback

# dearpygui related
NEW_VIEWPORT_HEIGHT = 1000
NEW_VIEWPORT_WIDTH = 1300
CHAT_ROOM_ID = "Chat Room"
CHAT_BOX_ID = "Chat Box"
CHAT_INPT_BOX_ID = " Chat Input Box"
CHAT_INPT_ID = "Chat Input"
SEND_BTN_ID = "Send Button"
ONLINE_LST_ID = "Online List"
WORD_WRAP_CNT = 850

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


# this is the client app
class ChatRoom:
    def __init__(self, dpg, username):
        # create client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(CLIENT_ADDR)  # connects to server

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
        # receive any messages sent to it by the server
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
                            self.send_msg(self.username)
                        else:
                            # update to gui (checks to see if the gui has been updated properly)
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
                        self.client.close()
                        break

        # closes the client's socket when the app is closed
        self.client.close()
        exit(0)

    # this method is used when we want to send the message from the input field
    def send(self):
        msg = f"{self.username} : {self.dpg.get_value(CHAT_INPT_ID)}"

        self.dpg.add_text(parent=CHAT_BOX_ID,
                          default_value=msg,
                          wrap=WORD_WRAP_CNT)

        self.dpg.set_value(CHAT_INPT_ID, "")

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
        self.send_msg(DISCONNECT_MESSAGE)

        self.dpg.set_viewport_height(700)
        self.dpg.set_viewport_width(1100)

        self.dpg.show_item("Name-Settings")
        self.dpg.delete_item(CHAT_ROOM_ID)

    # front-end (gui portion)
    def create_chat_room_win(self):
        # Chat Room Window
        # todo: adjust the height and width of the chat room
        with self.dpg.window(label="Chat Room",
                             id=CHAT_ROOM_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width()):
            chat_rm_height = self.dpg.get_viewport_configuration(CHAT_ROOM_ID).get('height')
            chat_rm_width = self.dpg.get_viewport_configuration(CHAT_ROOM_ID).get('width')

            with self.dpg.menu_bar():
                self.dpg.add_menu_item(label="Exit",
                                       callback=self.exit_callback)

            # Child 1: Online List (who is connected)
            with self.dpg.child(label="Online List",
                                id=ONLINE_LST_ID,
                                height=chat_rm_height * 0.85,
                                width=chat_rm_width * 0.15):
                self.dpg.add_text(default_value="Connected Users")

            self.dpg.add_same_line()
            with self.dpg.child(label="Chat Container",
                                height=chat_rm_height * 0.85,
                                width=chat_rm_width * 0.80):
                child_container_height = chat_rm_height
                child_container_width = chat_rm_width * 0.95

                # Child 2: Chat Box
                with self.dpg.child(label="Chat Box",
                                    id=CHAT_BOX_ID,
                                    height=child_container_height * 0.70,
                                    width=child_container_width * 0.80):
                    self.dpg.set_y_scroll(CHAT_BOX_ID, 1000)

                # Child 3: Input Box
                Tools.add_padding(self.dpg, 0, 15, False)
                with self.dpg.child(id=CHAT_INPT_BOX_ID,
                                    height=child_container_height * 0.10,
                                    width=child_container_width * 0.80):
                    Tools.add_padding(self.dpg, 75, 25, True)
                    self.dpg.add_input_text(id=CHAT_INPT_ID,
                                            width=725)
                    self.dpg.add_same_line()
                    self.dpg.add_button(label="Send",
                                        id=SEND_BTN_ID,
                                        callback=self.send)

    def listen_to_keys(self):
        while self.isRunning:
            if self.dpg.is_key_pressed(self.dpg.mvKey_Return) and self.dpg.is_item_focused(CHAT_INPT_ID):
                if not Tools.isBlank(self.dpg.get_value(CHAT_INPT_ID)):
                    self.send()
                    self.dpg.focus_item(CHAT_INPT_ID)  # reassigns focus back to the chat input field