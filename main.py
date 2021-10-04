import dearpygui.dearpygui as dpg
from nameconfig import NameConfig

# static vars
VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1100
VIEWPORT_TITLE = "(DearPyGUI) Chat Room"


def create_window():
    dpg.setup_viewport()
    dpg.set_viewport_title(VIEWPORT_TITLE)
    dpg.set_viewport_height(VIEWPORT_HEIGHT)
    dpg.set_viewport_width(VIEWPORT_WIDTH)

    # adding fonts
    create_dpg_fonts()

    # adding default themes
    create_dpg_themes()

    # creates the name settings window
    NameConfig(dpg)
    dpg.start_dearpygui()


def create_dpg_fonts():
    with dpg.font_registry():
        dpg.add_font("resources/fonts/Neon.ttf", 20, default_font=True)


def create_dpg_themes():
    with dpg.theme(default_theme=True):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (58, 37, 113), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (181, 170, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (10, 174, 23, 125), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (6, 4, 89), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 10)


if __name__ == "__main__":
    create_window()
    # print("Main Thread Ended")
