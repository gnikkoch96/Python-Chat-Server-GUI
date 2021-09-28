from chat_room import ChatRoom

NAME_SETTINGS_ID = "Name-Settings"
NAME_INPUT_ID = "Nickname"
JOIN_CHAT_BUTTON_ID = "Join Chat Room"


class NameConfig:
    def __init__(self, dpg):
        self.dpg = dpg

        # Name-Settings Window
        with self.dpg.window(label="Enter Name",
                             id=NAME_SETTINGS_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True):
            # Enter Name Input Field
            self.dpg.add_input_text(label="Enter Nickname:",
                                    id=NAME_INPUT_ID)
            # Join Chat Room Button
            self.dpg.add_button(label="Join Chat Room!",
                                id=JOIN_CHAT_BUTTON_ID,
                                callback=self.join_btn_callback)

    def join_btn_callback(self):
        # todo: check to see if there is text in the name input field, if not then the user can not join the room w/out a name

        # delete this window
        self.dpg.hide_item(NAME_SETTINGS_ID)

        # load chat room
        ChatRoom(self.dpg, self.dpg.get_value(NAME_INPUT_ID))
