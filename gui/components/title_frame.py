from tkinter import LEFT, TOP, Frame, Label
from gui.components.generic_entry import GenericEntry
from gui.components.generic_label import GenericLabel
import gui.main_window as mainwindow
from gui.components.generic_button import GenericButton

class TitleFrame(Frame):
    def __init__(self, master, title, *args, **kwargs):
        super().__init__(master, background=mainwindow.MAIN_BG, *args, **kwargs)
        self.title = Label(self, text=title, font=mainwindow.FONT_TITLE, background=mainwindow.MAIN_BG)
        self.title.pack(side=TOP, fill="x", expand=True, pady=15)
        self.titleSeparator = Frame(self, height=1, background=mainwindow.SIDE_MENU_BG)
        self.titleSeparator.pack(side=TOP, fill="x", padx=150, pady=(0, 25))