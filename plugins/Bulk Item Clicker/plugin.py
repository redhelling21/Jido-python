import ctypes
import pathlib
import time
from core.plugin_core import PluginCore
from tkinter import LEFT, Entry, Frame, Label, TOP, PhotoImage, StringVar, ttk
import customtkinter
from core.plugin_manager import PluginManager
from gui.components.generic_button import GenericButton
from gui.components.hotkey_frame import HotKeyFrame
import gui.main_window as mainwindow
from PIL import Image
from plugins.Autoloot.autoloot_thread import AutoLootThread
from gui.components.title_frame import TitleFrame
from gui.components.generic_label import GenericLabel
import keyboard
import mouse
import yaml
import numpy as np
from PIL import ImageGrab
import cv2
import os 
from scalpl import Cut

class Plugin(PluginCore):
    def __init__(self, config):
        self.config=config
        self.configProxy=Cut(config)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.corner = cv2.imread(dir_path + '/assets/corner.png')
        keyboard.add_hotkey(self.configProxy['pluginConfig.BulkItemClicker.mode1Hotkey'], self.mode_1)
        keyboard.add_hotkey(self.configProxy['pluginConfig.BulkItemClicker.mode2Hotkey'], self.mode_2)

    def get_frame(self, master):
        self.master = master
        self.frame = Frame(master)
        self.titleFrame = TitleFrame(self.frame, 'Bulk Item Clicker')
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        labelString = """
        Clique sur l'ensemble des items filtrés d'un stash. Il y a plusieurs modes.
        Mode 1 : prend la currency sous le curseur au moment de l'activation, et l'utilise sur les items filtrés.
        Mode 2 : ctrl+click les items filtrés."""
        self.descriptionLabel = GenericLabel(self.frame, text=labelString)
        self.descriptionLabel.pack(side=TOP)
        self.hotKeyFrame = HotKeyFrame(self.frame, 'pluginConfig.BulkItemClicker.mode1Hotkey', "Mode 1 :", self.mode_1, self.config, pady=40)
        self.hotKeyFrame.pack(side=TOP)
        self.hotKeyFrame2 = HotKeyFrame(self.frame, 'pluginConfig.BulkItemClicker.mode2Hotkey', "Mode 2 :", self.mode_2, self.config, pady=40)
        self.hotKeyFrame2.pack(side=TOP)
        return self.frame

    def mode_1(self):
        self.bulk_click_items(1)

    def mode_2(self):
        self.bulk_click_items(2)

    def bulk_click_items(self, mode):
        img = np.array(ImageGrab.grab())
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        res = cv2.matchTemplate(img, self.corner, cv2.TM_SQDIFF_NORMED)
        threshold = 0.05
        loc = np.where(res <= threshold)
        lastY = 0
        if mode == 1:
            mouse.press('right')
            time.sleep(0.02)
            mouse.release('right')
            keyboard.press('maj')
        if mode == 2:
            keyboard.press('ctrl')
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            temp = pt[1] - lastY
            if temp > 5 or temp == 0:
                lastY = pt[1]
                mouse.move(int(pt[0]), int(pt[1]))
                mouse.press() # left down
                time.sleep(0.02)
                mouse.release()
                time.sleep(0.2)
        
        if mode == 1:
            keyboard.release('maj')
        
        if mode == 2:
            keyboard.release('ctrl')