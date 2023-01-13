import pathlib, os
from core.plugin_core import PluginCore
from tkinter import Entry, Frame, Label, TOP, PhotoImage, ttk
import customtkinter
from core.plugin_manager import PluginManager
from gui.main_window import MAIN_BG, SIDE_MENU_BG
from PIL import Image

class Plugin(PluginCore):
    def __init__(self, pluginManager):
        self.pluginManager = pluginManager

    def get_frame(self, master):
        self.font_table_heading = customtkinter.CTkFont(family="Inter V Medium", size=14)
        self.font_table = customtkinter.CTkFont(family="Inter V Medium", size=12)
        self.font_small = customtkinter.CTkFont(family="Inter V Medium", size=16)
        self.font_big = customtkinter.CTkFont(family="Inter", size=30)
        self.frame = Frame(master)
        self.title = Label(self.frame, text="Général", font=self.font_big, background=MAIN_BG)
        self.title.pack(side=TOP, fill="x", expand=True, pady=15)
        self.titleSeparator = Frame(self.frame, height=1, background=SIDE_MENU_BG)
        self.titleSeparator.pack(side=TOP,fill="x", padx=150)

        self.currentLocation = pathlib.Path(__file__).parent.resolve()
        self.imgChecked = PhotoImage(file=self.currentLocation.joinpath('assets/checked.png'))
        self.imgUnChecked = PhotoImage(file=self.currentLocation.joinpath('assets/unchecked.png'))
        self.pluginTable = ttk.Treeview(self.frame, columns=(1, 2, 3))
        self.pluginTableStyle = ttk.Style(self.pluginTable)
        self.pluginTableStyle.configure("Treeview.Heading", font=(self.font_table_heading))
        self.pluginTableStyle.configure('Treeview', rowheight=24)
        self.pluginTable.tag_configure('checked', image=self.imgChecked)
        self.pluginTable.tag_configure('unchecked', image=self.imgUnChecked)

        self.pluginTable.heading(1, text="Nom")
        self.pluginTable.heading(2, text="Description")
        self.pluginTable.heading(3, text="Version")

        self.pluginTable.pack(side=TOP)
        self.pluginTable.bind('<Button 1>', self.checkRow)
        max_name_width = 0
        max_version_width = 0
        for pluginName, pluginInfos in self.pluginManager.get_available_plugins().items():
            name = pluginName
            version = pluginInfos.pluginVersion
            max_name_width = max(max_name_width, self.font_table.measure(str(pluginName)))
            max_version_width = max(max_version_width, self.font_table.measure(str(pluginInfos.pluginVersion)))
            self.pluginTable.insert('', 'end', value=(pluginName, pluginInfos.pluginDescription, pluginInfos.pluginVersion), tags="checked" if pluginInfos.isLoaded else "unchecked")

        self.pluginTable.column('#0', stretch='no', width=60)
        self.pluginTable.column('#1', stretch='no', width=max(max_name_width, 60))
        self.pluginTable.column('#2', stretch='yes', width=350)
        self.pluginTable.column('#3', stretch='no', width=max(max_version_width, 60))

        return self.frame

    def checkRow(self, event):
        rowId = self.pluginTable.identify_row(event.y)
        #TODO Simplifier
        tag = self.pluginTable.item(rowId, "tags")[0]
        tags = list(self.pluginTable.item(rowId, "tags"))
        tags.remove(tag)
        self.pluginTable.item(rowId, tags=tags)
        if tag == "checked":
            self.pluginTable.item(rowId, tags="unchecked")
        else:
            self.pluginTable.item(rowId, tags="checked")