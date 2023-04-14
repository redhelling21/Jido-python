from customtkinter import CTkButton
from gui.constants import *

class GenericButton(CTkButton):
    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master=master,
            fg_color=SIDE_MENU_BG,
            hover_color=SIDE_MENU_BG_ACTIVE_HOVER,
            corner_radius=5,
            font=FONT_COMPONENT,
            cursor='hand2',
            *args,
            **kwargs)