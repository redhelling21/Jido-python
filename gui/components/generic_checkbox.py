from customtkinter import CTkCheckBox
from gui.constants import *

class GenericCheckBox(CTkCheckBox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,
        font=FONT_GENERAL,
        fg_color=SIDE_MENU_BG,
        hover_color='white',
        border_color=SIDE_MENU_BG,
        checkbox_width=20,
        checkbox_height=20,
        text_color='black',
        border_width=2,
        onvalue='1',
        offvalue='0',
        *args,
        **kwargs)