from customtkinter import CTkCheckBox
import gui.main_window as mainwindow

class GenericCheckBox(CTkCheckBox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,
        font=mainwindow.FONT_GENERAL,
        fg_color=mainwindow.SIDE_MENU_BG,
        hover_color='white',
        border_color=mainwindow.SIDE_MENU_BG,
        checkbox_width=20,
        checkbox_height=20,
        text_color='black',
        border_width=2,
        onvalue='1',
        offvalue='0',
        *args,
        **kwargs)