import pathlib, os
import time
from core.plugin_core import PluginCore
from tkinter import LEFT, Entry, Frame, Label, TOP, PhotoImage, StringVar, ttk
import customtkinter
from core.plugin_manager import PluginManager
from gui.main_window import MAIN_BG, SIDE_MENU_BG, SIDE_MENU_BG_ACTIVE_HOVER
from PIL import Image
from plugins.Autoloot.autoloot_thread import AutoLootThread
import keyboard
import yaml

class Plugin(PluginCore):
    def __init__(self, pluginManager):
        self.pluginManager = pluginManager
        self.currentDir = str(pathlib.Path(__file__).parent.resolve())
        with open(self.currentDir + "\plugin_config.yml", "r") as f:
            config = yaml.safe_load(f)
        self.autolootKey = config["hotkey"]
        self.autolootThread = AutoLootThread()
        keyboard.add_hotkey('maj', self.toggle_autoloot)
        self.autolootThread.start()

    def get_frame(self, master):
        self.master = master
        self.font_small = customtkinter.CTkFont(family="Inter V Medium", size=16)
        self.font_big = customtkinter.CTkFont(family="Inter", size=30)
        self.frame = Frame(master)
        self.title = Label(self.frame, text="Autoloot", font=self.font_big, background=MAIN_BG)
        self.title.pack(side=TOP, fill="x", expand=True, pady=15)
        self.titleSeparator = Frame(self.frame, height=1, background=SIDE_MENU_BG)
        self.titleSeparator.pack(side=TOP,fill="x", padx=150)
        self.hotKeyFrame = Frame(self.frame, pady=40, background=MAIN_BG)
        self.hotKeyFrame.pack(side=TOP)
        self.hotKeyLabel = Label(self.hotKeyFrame, font=self.font_small, background=MAIN_BG, text=self.autolootKey)
        self.hotKeyButton = customtkinter.CTkButton(self.hotKeyFrame, text="Modifier", command=self.autoloot_key_choice, hover_color=SIDE_MENU_BG_ACTIVE_HOVER, fg_color=SIDE_MENU_BG)
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
        with open(self.currentDir + "\plugin_config.yml", 'w') as f:
            yaml.dump({'hotkey': self.autolootKey}, f)
        keyboard.remap_hotkey(self.autolootKey, tempkey)
        self.autolootKey = tempkey
        self.hotKeyLabel.configure(text=self.autolootKey)
        self.hotKeyButton.configure(text="Modifier") 
