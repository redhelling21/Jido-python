from tkinter import Label
import gui.main_window as mainwindow

class GenericLabel(Label):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,
        font=mainwindow.FONT_GENERAL,
        background=mainwindow.MAIN_BG,
        *args,
        **kwargs)