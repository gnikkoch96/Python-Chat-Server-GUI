class Tools:
    @staticmethod
    def add_padding(dpg, width_value=0, height_value=0, is_same_line=False):
        if height_value != 0:
            dpg.add_dummy(height=height_value)

        if width_value != 0:
            dpg.add_dummy(width=width_value)

        if is_same_line:
            dpg.add_same_line()

    @staticmethod
    def add_and_load_image(dpg, image_path, parent=None):
        width, height, channels, data = dpg.load_image(image_path)

        with dpg.texture_registry() as reg_id:
            texture_id = dpg.add_static_texture(width, height, data, parent=reg_id)

        if parent is None:
            return dpg.add_image(texture_id)
        else:
            return dpg.add_image(texture_id, parent=parent)

    @staticmethod
    # msg - message to be sent
    # header - the size of the header that contains info about the message length
    # msg_format - utf-8
    def format_msg_send(msg, header, msg_format):
        send_msg = msg.encode(msg_format)
        send_msg_len_info = len(send_msg)
        send_msg_len = str(send_msg_len_info).encode(msg_format)
        send_msg_len += b' ' * (header - len(send_msg_len))  # pads the header

        return send_msg, send_msg_len

    @staticmethod
    # checks if a string is blank and that it is not None type
    def isBlank(myString):
        if myString and myString.strip():
            # myString is not None AND myString is not empty or blank
            return False
        # myString is None OR myString is empty or blank
        return True
