import ctypes
import time
from core.plugin_core import PluginCore
from tkinter import Frame, TOP
from gui.components.generic_button import GenericButton
from gui.components.hotkey_frame import HotKeyFrame
from gui.constants import MAIN_BG
from gui.components.title_frame import TitleFrame
from gui.components.generic_label import GenericLabel
import keyboard
import mouse
import yaml
from scalpl import Cut


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class Plugin(PluginCore):
    def __init__(self, config):
        self.config = config
        self.configProxy = Cut(config)
        self.tradePosition = POINT()
        self.bottomCornerPosition = POINT()
        self.tradePosition.x = self.configProxy["pluginConfig.DivcardHandler.tradePosition.x"]
        self.tradePosition.y = self.configProxy["pluginConfig.DivcardHandler.tradePosition.y"]
        keyboard.add_hotkey(self.configProxy["pluginConfig.DivcardHandler.rewardHotkey"], self.get_stack_reward)
        keyboard.add_hotkey(self.configProxy["pluginConfig.DivcardHandler.deckHotkey"], self.use_stacked_deck)

    def get_frame(self, master):
        self.master = master
        self.frame = Frame(master)
        self.titleFrame = TitleFrame(self.frame, "Divcard handler")
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        labelString = """
        Utilise les stack decks, et rend les stacks complètes de divination cards.
        Avant utilisation, il faut paramétrer la position du bouton 'Trade'.
        Utiliser les stacked decks : lancer la macro en visant un stacked deck (attention, stacks de 10 uniquement)
        Rendre les stacks : lancer la macro en visant une stack complète"""
        self.descriptionLabel = GenericLabel(self.frame, text=labelString)
        self.descriptionLabel.pack(side=TOP)
        self.deckHotKeyFrame = HotKeyFrame(
            self.frame, "pluginConfig.DivcardHandler.deckHotkey", "Utiliser un stacked deck :", self.use_stacked_deck, self.config, pady=40
        )
        self.deckHotKeyFrame.pack(side=TOP)
        self.rewardHotKeyFrame = HotKeyFrame(
            self.frame, "pluginConfig.DivcardHandler.rewardHotkey", "Rendre une stack :", self.get_stack_reward, self.config, pady=40
        )
        self.rewardHotKeyFrame.pack(side=TOP)
        self.tradePositionFrame = Frame(self.frame, background=MAIN_BG)
        self.tradePositionFrame.pack(side=TOP)
        topCorner = "Position : " + str(self.tradePosition.x) + ", " + str(self.tradePosition.y)
        self.tradePositionLabel = GenericLabel(self.tradePositionFrame, text=topCorner)
        self.tradePositionLabel.pack(side=TOP)
        self.tradePositionButton = GenericButton(self.tradePositionFrame, text="Modifier...", command=self.select_trade_position)
        self.tradePositionButton.pack(side=TOP)
        return self.frame

    def use_stacked_deck(self):
        deckPos = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(deckPos))
        loops = 0
        while loops < 11:
            loops += 1
            mouse.press("right")  # left down
            time.sleep(0.02)
            mouse.release("right")
            time.sleep(0.1)
            mouse.move(int(deckPos.x - 1000), int(deckPos.y))
            time.sleep(0.1)
            mouse.press()  # left down
            time.sleep(0.02)
            mouse.release()
            time.sleep(0.1)
            mouse.move(int(deckPos.x), int(deckPos.y))

    def get_stack_reward(self):
        stackPos = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(stackPos))
        keyboard.release("maj")
        keyboard.press("ctrl")
        mouse.press()  # left down
        time.sleep(0.2)
        mouse.release()
        time.sleep(0.5)
        mouse.move(int(self.tradePosition.x), int(self.tradePosition.y))
        time.sleep(0.5)
        mouse.press()  # left down
        time.sleep(0.2)
        mouse.release()
        time.sleep(0.5)
        mouse.move(int(self.tradePosition.x), int(self.tradePosition.y - 200))
        time.sleep(0.5)
        mouse.press()  # left down
        time.sleep(0.2)
        mouse.release()
        mouse.move(int(stackPos.x), int(stackPos.y))
        keyboard.release("ctrl")

    def select_trade_position(self):
        self.tradePositionButton.configure(text="Capture dans 3...")
        self.master.update_idletasks()
        time.sleep(1)
        self.tradePositionButton.configure(text="Capture dans 2...")
        self.master.update_idletasks()
        time.sleep(1)
        self.tradePositionButton.configure(text="Capture dans 1...")
        self.master.update_idletasks()
        time.sleep(1)
        tpoint = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(tpoint))
        self.tradePositionLabel.configure(text="Position : " + str(tpoint.x) + ", " + str(tpoint.y))
        self.tradePositionButton.configure(text="Modifier...")
        self.master.update_idletasks()

        self.tradePosition.x = tpoint.x
        self.tradePosition.y = tpoint.y

        self.configProxy["pluginConfig.DivcardHandler.tradePosition.x"] = tpoint.x
        self.configProxy["pluginConfig.DivcardHandler.tradePosition.y"] = tpoint.y
        with open("config.yml", "w") as f:
            yaml.dump(self.config, f)
