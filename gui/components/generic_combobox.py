from customtkinter import CTkComboBox
from gui.constants import *

class GenericComboBox(CTkComboBox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,
        text_color="#000000",
        border_color=SIDE_MENU_BG,
        fg_color=MAIN_BG,
        button_color=SIDE_MENU_BG,
        button_hover_color=SIDE_MENU_BG_ACTIVE_HOVER,
        corner_radius=5,
        dropdown_fg_color=MAIN_BG,
        dropdown_hover_color=SIDE_MENU_BG_ACTIVE_HOVER,
        dropdown_text_color="#000000",
        font=FONT_COMPONENT,
        *args,
        **kwargs)