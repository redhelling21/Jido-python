import pathlib
from core.plugin_core import PluginCore
from tkinter import LEFT, Entry, Frame, Label, TOP, PhotoImage, StringVar, ttk
import customtkinter
from core.plugin_manager import PluginManager
from gui.components.generic_button import GenericButton
from gui.components.generic_checkbox import GenericCheckBox
from gui.components.generic_label import GenericLabel
from gui.components.hotkey_frame import HotKeyFrame
from gui.constants import *
from PIL import Image
from plugins.Autoloot.autoloot_thread import AutoLootThread
from gui.components.title_frame import TitleFrame
import keyboard
import yaml
from scalpl import Cut


class Plugin(PluginCore):
    def __init__(self, config):
        self.config = config
        self.toggleMacro = False
        self.configProxy = Cut(config)
        self.autolootThread = AutoLootThread()
        keyboard.add_hotkey(self.configProxy["pluginConfig.Autoloot.hotkey"], self.toggle_autoloot)
        self.autolootThread.start()

    def get_frame(self, master):
        self.master = master
        self.frame = Frame(master)
        self.shouldClickExpedition = StringVar(self.frame, self.configProxy.get("pluginConfig.Autoloot.chests.expedition", "0"))
        self.shouldClickBlight = StringVar(self.frame, self.configProxy.get("pluginConfig.Autoloot.chests.blight", "0"))
        self.shouldClickLegion = StringVar(self.frame, self.configProxy.get("pluginConfig.Autoloot.chests.legion", "0"))
        self.shouldClickHeist = StringVar(self.frame, self.configProxy.get("pluginConfig.Autoloot.chests.heist", "0"))
        self.shouldClickBreach = StringVar(self.frame, self.configProxy.get("pluginConfig.Autoloot.chests.breach", "0"))
        self.titleFrame = TitleFrame(self.frame, "Autoloot")
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        labelString = """
        Clique automatiquement sur les loots encadrés d'une couleur spécifique (#FE00FE).
        Dispose d'une option pour cliquer automatiquement sur les coffres spéciaux (expedition, blight...).
        """
        self.descriptionLabel = GenericLabel(self.frame, text=labelString)
        self.descriptionLabel.pack(side=TOP)
        self.hotKeyFrame = HotKeyFrame(self.frame, "pluginConfig.Autoloot.hotkey", "Activer l'autoloot :", self.toggle_autoloot, self.config)
        self.hotKeyFrame.pack(side=TOP)
        self.chestsLabel = GenericLabel(self.frame, text="Clics sur les coffres spéciaux (~5ms chacun):")
        self.chestsLabel.pack(side=TOP, pady=(15, 5))
        self.chestsFrame = Frame(self.frame, background=MAIN_BG)
        self.chestsFrame.pack(side=TOP)

        self.expeditionCheckBox = GenericCheckBox(self.chestsFrame, text="Expedition chests", variable=self.shouldClickExpedition)
        self.expeditionCheckBox.pack(side=TOP, anchor="w")
        self.blightCheckBox = GenericCheckBox(self.chestsFrame, text="Blighted chests", variable=self.shouldClickBlight)
        self.blightCheckBox.pack(side=TOP, anchor="w")
        self.breachCheckBox = GenericCheckBox(self.chestsFrame, text="Breach hands", variable=self.shouldClickBreach)
        self.breachCheckBox.pack(side=TOP, anchor="w")
        self.heistCheckBox = GenericCheckBox(self.chestsFrame, text="Smuggler's caches", variable=self.shouldClickHeist)
        self.heistCheckBox.pack(side=TOP, anchor="w")
        self.legionCheckBox = GenericCheckBox(self.chestsFrame, text="Legion warhoards", variable=self.shouldClickLegion)
        self.legionCheckBox.pack(side=TOP, anchor="w")

        self.saveChestsButton = GenericButton(self.frame, text="Sauver", command=self.save_config)
        self.saveChestsButton.pack(side=TOP, pady=15)
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

    def save_config(self):
        self.autolootThread.lootBlight = int(self.shouldClickBlight.get())
        self.autolootThread.lootLegion = int(self.shouldClickLegion.get())
        self.autolootThread.lootHeist = int(self.shouldClickHeist.get())
        self.autolootThread.lootBreach = int(self.shouldClickBreach.get())
        self.autolootThread.lootExpedition = int(self.shouldClickExpedition.get())
        chests = {}
        chests["blight"] = self.shouldClickBlight.get()
        chests["legion"] = self.shouldClickLegion.get()
        chests["heist"] = self.shouldClickHeist.get()
        chests["breach"] = self.shouldClickBreach.get()
        chests["expedition"] = self.shouldClickExpedition.get()
        self.configProxy["pluginConfig.Autoloot.chests"] = chests
        with open("config.yml", "w") as f:
            yaml.dump(self.config, f)