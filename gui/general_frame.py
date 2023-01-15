from tkinter import *
from tkinter import ttk
from gui.components.generic_button import GenericButton
from gui.components.generic_entry import GenericEntry
from gui.components.generic_label import GenericLabel
from gui.components.generic_combobox import GenericComboBox
from gui.components.title_frame import TitleFrame
import gui.main_window as mainwindow

class GeneralFrame(Frame):
    def __init__(self, config, pluginmanager, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pluginManager = pluginmanager
        self.titleFrame = TitleFrame(self, 'Général')
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        self.pluginPackSelection = Frame(self, background=mainwindow.MAIN_BG)
        self.pluginPackSelection.pack(side=TOP, pady=(0, 20))
        self.pluginPackSelectionLabel = GenericLabel(self.pluginPackSelection, text='Choisir un pack :')
        self.pluginPackSelectionLabel.pack(side=LEFT)
        self.pluginPackSelectionBox = GenericComboBox(self.pluginPackSelection, values=["option 1", "option 2"])
        self.pluginPackSelectionBox.pack(side=LEFT, padx=10)
        self.pluginPackSelectionButton = GenericButton(self.pluginPackSelection, text="Charger")
        self.pluginPackSelectionButton.pack(side=LEFT)

        self.imgChecked = PhotoImage(file='gui/assets/checked.png')
        self.imgUnChecked = PhotoImage(file='gui/assets/unchecked.png')
        self.pluginTable = ttk.Treeview(self, columns=(1, 2, 3))
        self.pluginTableStyle = ttk.Style(self.pluginTable)
        self.pluginTableStyle.configure("Treeview.Heading", font=mainwindow.FONT_TABLE_HEADING)
        self.pluginTableStyle.configure('Treeview', rowheight=24)
        self.pluginTable.tag_configure('checked', image=self.imgChecked)
        self.pluginTable.tag_configure('checked', font=mainwindow.FONT_TABLE)
        self.pluginTable.tag_configure('unchecked', image=self.imgUnChecked)
        self.pluginTable.tag_configure('unchecked', font=mainwindow.FONT_TABLE)

        self.pluginTable.heading(1, text="Nom")
        self.pluginTable.heading(2, text="Description")
        self.pluginTable.heading(3, text="Version")

        self.pluginTable.pack(side=TOP, pady=(0, 20))
        self.pluginTable.bind('<Button 1>', self.checkRow)
        max_name_width = 0
        max_version_width = 0
        for pluginName, pluginInfos in self.pluginManager.get_available_plugins().items():
            name = pluginName
            version = pluginInfos.pluginVersion
            max_name_width = max(max_name_width, mainwindow.FONT_TABLE.measure(str(pluginName)))
            max_version_width = max(max_version_width, mainwindow.FONT_TABLE.measure(str(pluginInfos.pluginVersion)))
            self.pluginTable.insert('', 'end', value=(pluginName, pluginInfos.pluginDescription, pluginInfos.pluginVersion), tags="checked" if pluginInfos.isLoaded else "unchecked")

        self.pluginTable.column('#0', stretch='no', width=60)
        self.pluginTable.column('#1', stretch='no', width=max(max_name_width, 60))
        self.pluginTable.column('#2', stretch='yes', width=350)
        self.pluginTable.column('#3', stretch='no', width=max(max_version_width, 60))

        self.pluginPackCreation = Frame(self, background=mainwindow.MAIN_BG)
        self.pluginPackCreation.pack(side=TOP)
        self.pluginPackCreationLabel = GenericLabel(self.pluginPackCreation, text='Enregistrer : ')
        self.pluginPackCreationLabel.pack(side=LEFT)
        self.pluginPackCreationEntry = GenericEntry(self.pluginPackCreation)
        self.pluginPackCreationEntry.pack(side=LEFT, padx=10)
        self.pluginPackCreationButton = GenericButton(self.pluginPackCreation, text="Enregistrer")
        self.pluginPackCreationButton.pack(side=LEFT)

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