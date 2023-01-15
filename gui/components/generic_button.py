from customtkinter import CTkButton
import gui.main_window as mainwindow

class GenericButton(CTkButton):
    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master=master,
            fg_color=mainwindow.SIDE_MENU_BG,
            hover_color=mainwindow.SIDE_MENU_BG_ACTIVE_HOVER,
            corner_radius=5,
            font=mainwindow.FONT_COMPONENT,
            cursor='hand2',
            *args,
            **kwargs)