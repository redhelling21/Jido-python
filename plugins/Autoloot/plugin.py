import pathlib
from core.plugin_core import PluginCore
from tkinter import LEFT, Entry, Frame, Label, TOP, PhotoImage, StringVar, ttk
import customtkinter
from core.plugin_manager import PluginManager
from gui.components.generic_button import GenericButton
from gui.components.generic_label import GenericLabel
from gui.components.hotkey_frame import HotKeyFrame
import gui.main_window as mainwindow
from PIL import Image
from plugins.Autoloot.autoloot_thread import AutoLootThread
from gui.components.title_frame import TitleFrame
import keyboard
import yaml
from scalpl import Cut

class Plugin(PluginCore):
    def __init__(self, config):
        self.config=config
        self.toggleMacro = False
        self.configProxy=Cut(config)
        self.autolootThread = AutoLootThread()
        keyboard.add_hotkey(self.configProxy['pluginConfig.Autoloot.hotkey'], self.toggle_autoloot)
        self.autolootThread.start()

    def get_frame(self, master):
        self.master = master
        self.frame = Frame(master)
        self.titleFrame = TitleFrame(self.frame, 'Autoloot')
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        labelString = """
        Clique automatiquement sur les loots encadrés d'une couleur spécifique (#FE00FE).
        Dispose d'une option pour cliquer automatiquement sur les coffres spéciaux (expedition, blight...).
        """
        self.descriptionLabel = GenericLabel(self.frame, text=labelString)
        self.descriptionLabel.pack(side=TOP)
        self.hotKeyFrame = HotKeyFrame(self.frame, 'pluginConfig.Autoloot.hotkey', "Activer l'autoloot :", self.toggle_autoloot, self.config)
        self.hotKeyFrame.pack(side=TOP)
        return self.frame

    def toggle_autoloot(self):
        if (not self.autolootThread.autoloot.is_set()) and self.toggleMacro:  
            print("Autoloot ON")
            self.autolootThread.autoloot.set()
        else:
            print("Autoloot OFF")
            self.autolootThread.autoloot.clear()
    
    def toggle_macro(self, toggle):
        self.toggleMacro = toggle