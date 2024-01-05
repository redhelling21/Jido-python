from tkinter import TOP, Frame, Label
from gui.constants import MAIN_BG, FONT_TITLE, SIDE_MENU_BG


class TitleFrame(Frame):
    def __init__(self, master, title, *args, **kwargs):
        super().__init__(master, background=MAIN_BG, *args, **kwargs)
        self.title = Label(self, text=title, font=FONT_TITLE, background=MAIN_BG)
        self.title.pack(side=TOP, fill="x", expand=True, pady=15)
        self.titleSeparator = Frame(self, height=1, background=SIDE_MENU_BG)
        self.titleSeparator.pack(side=TOP, fill="x", padx=150, pady=(0, 25))
