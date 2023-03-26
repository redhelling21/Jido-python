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
from plugins.Autopress.autopress_thread import AutoPressThread
from gui.components.title_frame import TitleFrame
import keyboard
import yaml
from scalpl import Cut

class Plugin(PluginCore):
    def __init__(self, config):
        self.config=config
        self.toggleMacro = False
        self.configProxy=Cut(config)
        self.autopressThread = AutoPressThread()
        keyboard.add_hotkey(self.configProxy['pluginConfig.Autopress.hotkey'], self.toggle_autopress)
        self.autopressThread.start()

    def get_frame(self, master):
        self.master = master
        self.frame = Frame(master)
        self.titleFrame = TitleFrame(self.frame, 'Autopress')
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        labelString = """
        Appuie automatiquement sur les touches demandées.
        Si deux touches entrent en conflit, elles sont pressées dans l'ordre de la liste.
        """
        self.descriptionLabel = GenericLabel(self.frame, text=labelString)
        self.descriptionLabel.pack(side=TOP)
        self.hotKeyFrame = HotKeyFrame(self.frame, 'pluginConfig.Autopress.hotkey', "Activer l'autopress :", self.toggle_autopress, self.config)
        self.hotKeyFrame.pack(side=TOP)
        return self.frame

    def toggle_autopress(self):
        if (not self.autopressThread.autopress.is_set()) and self.toggleMacro:  
            print("Autopress ON")
            self.autopressThread.autopress.set()
        else:
            print("Autopress OFF")
            self.autopressThread.autopress.clear()
    
    def toggle_macro(self, toggle):
        self.toggleMacro = toggle