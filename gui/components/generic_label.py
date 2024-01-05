from tkinter import Label
from gui.constants import FONT_GENERAL, MAIN_BG


class GenericLabel(Label):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, font=FONT_GENERAL, background=MAIN_BG, *args, **kwargs)
