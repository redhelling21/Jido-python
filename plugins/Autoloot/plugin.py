import pathlib
from core.plugin_core import PluginCore
from tkinter import LEFT, Entry, Frame, Label, TOP, PhotoImage, StringVar, ttk
import customtkinter
from core.plugin_manager import PluginManager
from gui.components.generic_button import GenericButton
import gui.main_window as mainwindow
from PIL import Image
from plugins.Autoloot.autoloot_thread import AutoLootThread
from gui.components.title_frame import TitleFrame
import keyboard
import yaml

class Plugin(PluginCore):
    def __init__(self, config):
        self.config=config
        self.autolootKey = self.config['pluginConfig']['Autoloot']['hotkey']
        self.autolootThread = AutoLootThread()
        keyboard.add_hotkey(self.autolootKey, self.toggle_autoloot)
        self.autolootThread.start()

    def get_frame(self, master):
        self.master = master
        self.frame = Frame(master)
        self.titleFrame = TitleFrame(self.frame, 'Autoloot')
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        self.hotKeyFrame = Frame(self.frame, pady=40, background=mainwindow.MAIN_BG)
        self.hotKeyFrame.pack(side=TOP)
        self.hotKeyLabel = Label(self.hotKeyFrame, font=mainwindow.FONT_GENERAL, background=mainwindow.MAIN_BG, text=self.autolootKey)
        self.hotKeyButton = GenericButton(self.hotKeyFrame, text="Modifier", command=self.autoloot_key_choice)
        self.hotKeyLabel.pack(anchor="c")
        self.hotKeyButton.pack(anchor="c")
        
        return self.frame

    def toggle_autoloot(self):
        print("toggle autoloot")
        if self.autolootThread.autoloot.is_set():  
            self.autolootThread.autoloot.clear()
        else:
            self.autolootThread.autoloot.set()
    
    def autoloot_key_choice(self):
        self.hotKeyButton.configure(text="Taper un raccourci...")
        self.master.update_idletasks()
        tempkey = keyboard.read_hotkey()
        keyboard.remap_hotkey(self.autolootKey, tempkey)
        self.autolootKey = tempkey
        self.config['pluginConfig']['Autoloot']['hotkey'] = self.autolootKey
        with open("config.yml", 'w') as f:
            yaml.dump(self.config, f)
        self.hotKeyLabel.configure(text=self.autolootKey)
        self.hotKeyButton.configure(text="Modifier") 
