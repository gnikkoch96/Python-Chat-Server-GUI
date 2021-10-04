from chat_room import ChatRoom
from tools import Tools

NAME_SETTINGS_ID = "Name-Settings"
NAME_INPUT_ID = "Nickname"
JOIN_CHAT_BUTTON_ID = "Join Chat Room"


class NameConfig:
    def __init__(self, dpg):
        self.dpg = dpg

        # Name-Settings Window
        with self.dpg.window(label="Chatroom Settings",
                             id=NAME_SETTINGS_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True):

            Tools.add_padding(self.dpg, 50, 50, True)
            Tools.add_and_load_image(self.dpg, 'resources/imgs/banner.png')

            # Enter Name Input Field
            Tools.add_padding(self.dpg, 100, 50, True)
            self.dpg.add_text("Username: ")
            self.dpg.add_same_line()
            self.dpg.add_input_text(id=NAME_INPUT_ID)

            # Join Chat Room Button
            Tools.add_padding(self.dpg, 450, 50, True)
            self.dpg.add_button(label="Enter Chat Room",
                                id=JOIN_CHAT_BUTTON_ID,
                                callback=self.join_btn_callback)

            with self.dpg.tooltip(JOIN_CHAT_BUTTON_ID):
                self.dpg.add_text("Enter the Chatroom (Note: Make sure username is not empty)")

        self.dpg.set_primary_window(NAME_SETTINGS_ID, True)

    def join_btn_callback(self):
        username = self.dpg.get_value(NAME_INPUT_ID)

        if not Tools.isBlank(username):
            # hide this window
            self.dpg.hide_item(NAME_SETTINGS_ID)

            # load chat room
            ChatRoom(self.dpg, self.dpg.get_value(NAME_INPUT_ID))


