import dearpygui.dearpygui as dpg

def change_text(msg):
    print(msg)

with dpg.window(width=500, height=300):
    text_widget = dpg.add_text("Click me with any mouse button")
    dpg.add_button(callback=change_text, user_data="message")

dpg.start_dearpygui()