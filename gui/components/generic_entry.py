from customtkinter import CTkEntry
import gui.main_window as mainwindow

class GenericEntry(CTkEntry):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,
        fg_color=mainwindow.MAIN_BG,
        text_color="#000000",
        corner_radius=5,
        border_color=mainwindow.SIDE_MENU_BG,
        font=mainwindow.FONT_COMPONENT,
        *args,
        **kwargs)