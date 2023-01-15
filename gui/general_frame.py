from tkinter import *
from tkinter import ttk
import customtkinter
import gui.main_window as mainwindow
import pathlib

class GeneralFrame(Frame):
    def __init__(self, config, pluginmanager, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pluginManager = pluginmanager
        self.font_table_heading = customtkinter.CTkFont(family="Inter V Medium", size=14)
        self.font_table = customtkinter.CTkFont(family="Inter V Medium", size=12)
        self.font_small = customtkinter.CTkFont(family="Inter V Medium", size=16)
        self.font_big = customtkinter.CTkFont(family="Inter", size=30)
        self.title = Label(self, text="Général", font=self.font_big, background=mainwindow.MAIN_BG)
        self.title.pack(side=TOP, fill="x", expand=True, pady=15)
        self.titleSeparator = Frame(self, height=1, background=mainwindow.SIDE_MENU_BG)
        self.titleSeparator.pack(side=TOP,fill="x", padx=150)

        self.imgChecked = PhotoImage(file='gui/assets/checked.png')
        self.imgUnChecked = PhotoImage(file='gui/assets/unchecked.png')
        self.pluginTable = ttk.Treeview(self, columns=(1, 2, 3))
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