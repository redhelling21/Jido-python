from customtkinter import CTkButton
from tkinter import W
import gui.main_window as mainwindow

class MenuButton(CTkButton):
    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master=master, 
            anchor=W, 
            font=mainwindow.FONT_MENU,
            width=260,
            height=40,
            corner_radius=10,
            hover_color=mainwindow.SIDE_MENU_BG_ACTIVE_HOVER,
            cursor='hand2',
            *args, 
            **kwargs)