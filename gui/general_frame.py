from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from gui.components.generic_button import GenericButton
from gui.components.generic_entry import GenericEntry
from gui.components.generic_label import GenericLabel
from gui.components.generic_combobox import GenericComboBox
from gui.components.hotkey_frame import HotKeyFrame
from gui.components.title_frame import TitleFrame
from gui.constants import *
from array import array
import keyboard
import yaml

class GeneralFrame(Frame):
    def __init__(self, config, pluginmanager, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config = config
        self.toggleMacro = False
        self.pluginManager = pluginmanager
        self.titleFrame = TitleFrame(self, 'Général')
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        self.pluginPackGeneral = Frame(self, background=MAIN_BG)
        self.pluginPackGeneral.pack(side=TOP, pady=(0,20))
        self.pluginPackLabels = Frame(self.pluginPackGeneral, background=MAIN_BG)
        self.pluginPackLabels.pack(side=LEFT)
        self.pluginPackControls = Frame(self.pluginPackGeneral, background=MAIN_BG)
        self.pluginPackControls.pack(side=LEFT, padx=10)
        self.pluginPackButtons = Frame(self.pluginPackGeneral, background=MAIN_BG)
        self.pluginPackButtons.pack(side=LEFT)

        self.pluginPackSelectionLabel = GenericLabel(self.pluginPackLabels, text='Choisir un pack :')
        self.pluginPackSelectionLabel.pack(side=TOP, anchor="e", pady=(0,15))
        self.pluginPackCreationLabel = GenericLabel(self.pluginPackLabels, text='Enregistrer :')
        self.pluginPackCreationLabel.pack(side=TOP, anchor="e")

        self.loadedPluginPack = StringVar(value=config['activePluginPack'])
        self.pluginPackSelectionBox = GenericComboBox(self.pluginPackControls, values=list(config['pluginPacks'].keys()), variable=self.loadedPluginPack)
        self.pluginPackSelectionBox.pack(side=TOP, anchor="e", pady=(0,10))
        self.pluginPackCreationEntry = GenericEntry(self.pluginPackControls)
        self.pluginPackCreationEntry.pack(side=TOP, anchor="e")

        self.pluginPackSelectionButton = GenericButton(self.pluginPackButtons, text="Appliquer")
        self.pluginPackSelectionButton.pack(side=TOP, anchor="e", pady=(0,10))
        self.pluginPackCreationButton = GenericButton(self.pluginPackButtons, text="Enregistrer")
        self.pluginPackCreationButton.pack(side=TOP, anchor="e")

        self.imgChecked = PhotoImage(file='gui/assets/checked.png')
        self.imgUnChecked = PhotoImage(file='gui/assets/unchecked.png')
        self.pluginTable = ttk.Treeview(self, columns=(1, 2, 3))
        self.pluginTableStyle = ttk.Style(self.pluginTable)
        self.pluginTableStyle.configure("Treeview.Heading", font=FONT_TABLE_HEADING)
        self.pluginTableStyle.configure('Treeview', rowheight=24)
        self.pluginTable.tag_configure('checked', image=self.imgChecked)
        self.pluginTable.tag_configure('checked', font=FONT_TABLE)
        self.pluginTable.tag_configure('unchecked', image=self.imgUnChecked)
        self.pluginTable.tag_configure('unchecked', font=FONT_TABLE)

        self.pluginTable.heading(1, text="Nom")
        self.pluginTable.heading(2, text="Description")
        self.pluginTable.heading(3, text="Version")

        self.pluginTable.pack(side=TOP, pady=(0, 20))
        self.pluginTable.bind('<Button 1>', self.check_row)
        max_name_width = 0
        max_version_width = 0
        for pluginName, pluginInfos in self.pluginManager.get_available_plugins().items():
            name = pluginName
            version = pluginInfos.pluginVersion
            max_name_width = max(max_name_width, FONT_TABLE.measure(str(pluginName)))
            max_version_width = max(max_version_width, FONT_TABLE.measure(str(pluginInfos.pluginVersion)))
            self.pluginTable.insert('', 'end', value=(pluginName, pluginInfos.pluginDescription, pluginInfos.pluginVersion), tags="checked" if pluginInfos.isLoaded else "unchecked")

        self.pluginTable.column('#0', stretch='no', width=60)
        self.pluginTable.column('#1', stretch='no', width=max(max_name_width+10, 60))
        self.pluginTable.column('#2', stretch='yes', width=350)
        self.pluginTable.column('#3', stretch='no', width=max(max_version_width+10, 60))

        self.pluginLoading = Frame(self, background=MAIN_BG)
        self.pluginLoading.pack(side=TOP)
        self.pluginLoadingButton = GenericButton(self.pluginLoading, text="Charger les plugins sélectionnés")
        self.pluginLoadingButton.pack(side=TOP)

        keyboard.add_hotkey(self.config['generalActivationKey'], self.toggle_general_macro)
        self.hotKeyFrame = HotKeyFrame(self, 'generalActivationKey', 'Activer la macro :', self.toggle_general_macro, self.config, pady=40)
        self.hotKeyFrame.pack(side=TOP)

    def check_row(self, event):
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

    def toggle_general_macro(self):
        self.toggleMacro = not self.toggleMacro
        for plugin in self.pluginManager.get_loaded_plugins().items():
            plugin[1].toggle_macro(self.toggleMacro)
