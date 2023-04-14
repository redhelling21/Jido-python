from customtkinter import CTkEntry
from gui.constants import *

class GenericEntry(CTkEntry):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,
        fg_color=MAIN_BG,
        text_color="#000000",
        corner_radius=5,
        border_color=SIDE_MENU_BG,
        font=FONT_COMPONENT,
        *args,
        **kwargs)