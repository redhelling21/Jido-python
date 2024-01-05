from customtkinter import CTkButton
from tkinter import W
from gui.constants import FONT_MENU, SIDE_MENU_BG_ACTIVE_HOVER


class MenuButton(CTkButton):
    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master=master,
            anchor=W,
            font=FONT_MENU,
            width=260,
            height=40,
            corner_radius=10,
            hover_color=SIDE_MENU_BG_ACTIVE_HOVER,
            cursor="hand2",
            *args,
            **kwargs
        )
