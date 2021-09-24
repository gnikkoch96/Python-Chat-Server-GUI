import dearpygui.dearpygui as dpg
from nameconfig import NameConfig

# static vars
VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1000

def create_window():
    dpg.setup_viewport()
    dpg.set_viewport_title("(DearPyGUI) Chat Room")
    dpg.set_viewport_height(VIEWPORT_HEIGHT)
    dpg.set_viewport_width(VIEWPORT_WIDTH)
    NameConfig(dpg)
    dpg.start_dearpygui()

if __name__ == "__main__":
    create_window()