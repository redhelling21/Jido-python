from tkinter import LEFT, TOP, Frame, Label, StringVar
from gui.components.generic_button import GenericButton
from gui.components.generic_entry import GenericEntry
from gui.components.generic_label import GenericLabel
import gui.main_window as mainwindow
import keyboard
from scalpl import Cut
import yaml

class HotKeyFrame(Frame):
    def __init__(self, master, hotKeyConfigPath, hotKeyDescription, toggledFunction, config, *args, **kwargs):
        super().__init__(master, background=mainwindow.MAIN_BG, *args, **kwargs)
        self.hotKeyConfigPath = hotKeyConfigPath
        self.config = config
        self.toggledFunction = toggledFunction
        self.configProxy = Cut(self.config)
        self.hotkey = self.configProxy[self.hotKeyConfigPath]
        self.hotkeyVar = StringVar(master, self.hotkey)
        self.master = master
        self.hotKeyLabel = GenericLabel(self, text=hotKeyDescription)
        self.hotKeyEntry= GenericEntry(self, textvariable=self.hotkeyVar)
        self.hotKeyButton = GenericButton(self, text="Enregistrer", command=self.hotkey_choice)
        self.hotKeyLabel.pack(side=LEFT)
        self.hotKeyEntry.pack(side=LEFT, padx=10)
        self.hotKeyButton.pack(side=LEFT)
        
    def hotkey_choice(self):
        keyboard.remove_hotkey(self.hotkey)
        self.hotkey = self.hotkeyVar.get()
        keyboard.add_hotkey(self.hotkey, self.toggledFunction)
        self.configProxy[self.hotKeyConfigPath] = self.hotkey
        with open("config.yml", 'w') as f:
            yaml.dump(self.config, f)
        self.focus()