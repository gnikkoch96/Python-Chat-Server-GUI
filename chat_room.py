from tools import Tools

CHAT_ROOM_ID = "Chat Room"
CHAT_BOX_ID = "Chat Box"
CHAT_INPT_ID = "Chat Input"
ONLINE_LST_ID = "Online List"


class ChatRoom:
    def __init__(self, dpg, username):
        self.dpg = dpg
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
            # todo: replace this
            with self.dpg.child(label="Chat Container",
                                height=self.dpg.get_viewport_height(),
                                width=self.dpg.get_viewport_width() * 0.75):
                # Child 2: Chat Box
                with self.dpg.child(label="Chat Box",
                                     id=CHAT_BOX_ID,
                                     height=self.dpg.get_viewport_height() * 0.75,
                                     width=self.dpg.get_viewport_width() * 0.75):
                    # todo: find a way to dynamically add input fields to display messages
                    self.dpg.add_input_text(label="Dummy Chat Box")

                # Child 3: Input Box
                with self.dpg.child(label="Chat Input",
                                     id=CHAT_INPT_ID,
                                     height=self.dpg.get_viewport_height() * 0.25,
                                     width=self.dpg.get_viewport_width() * 0.75):
                    self.dpg.add_input_text(label="Dummy Input Box")
                    self.dpg.add_button(label="Send")
