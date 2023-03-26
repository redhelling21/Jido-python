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
import yaml
import numpy as np
from PIL import ImageGrab
import cv2
import os 
from scalpl import Cut
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class Plugin(PluginCore):
    def __init__(self, config):
        self.config=config
        self.configProxy=Cut(config)
        self.emptyInventoryPath = os.path.dirname(os.path.realpath(__file__)) + '/assets/empty_inv.png'
        self.emptyInventory = cv2.imread(self.emptyInventoryPath)
        self.topCornerPosition = POINT()
        self.bottomCornerPosition = POINT()
        self.topCornerPosition.x = self.configProxy['pluginConfig.InventoryEmptyer.inventoryPosition.topCorner.x']
        self.topCornerPosition.y = self.configProxy['pluginConfig.InventoryEmptyer.inventoryPosition.topCorner.y']
        self.bottomCornerPosition.x = self.configProxy['pluginConfig.InventoryEmptyer.inventoryPosition.bottomCorner.x']
        self.bottomCornerPosition.y = self.configProxy['pluginConfig.InventoryEmptyer.inventoryPosition.bottomCorner.y']


        keyboard.add_hotkey(self.configProxy['pluginConfig.InventoryEmptyer.hotkey'], self.empty_inventory)

    def get_frame(self, master):
        self.master = master
        self.frame = Frame(master)
        self.titleFrame = TitleFrame(self.frame, 'Inventory Emptyer')
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        labelString = """
        Vide l'inventaire en comparant l'inventaire vide avec l'inventaire actuel.
        Avant utilisation, il faut paramétrer la position de l'inventaire.
        Sélectionner le coin en haut à gauche puis le coin en bas à droite de la zone à vider.
        Attention : ne pas sélectionner l'ensemble de l'inventaire si vous voulez que certains colonnes ne soient pas traitées."""
        self.descriptionLabel = GenericLabel(self.frame, text=labelString)
        self.descriptionLabel.pack(side=TOP)
        self.hotKeyFrame = HotKeyFrame(self.frame, 'pluginConfig.InventoryEmptyer.hotkey', "Vider l'inventaire : ", self.empty_inventory, self.config, pady=40)
        self.hotKeyFrame.pack(side=TOP)
        self.inventoryPositionFrame = Frame(self.frame, background=mainwindow.MAIN_BG)
        self.inventoryPositionFrame.pack(side=TOP)
        topCorner = "Coin haut gauche : " + str(self.topCornerPosition.x) + ", " + str(self.topCornerPosition.y)
        bottomCorner = "Coin bas droite : " + str(self.bottomCornerPosition.x) + ", " + str(self.bottomCornerPosition.y)
        self.topCornerPositionLabel = GenericLabel(self.inventoryPositionFrame, text=topCorner)
        self.topCornerPositionLabel.pack(side=TOP)
        self.bottomCornerPositionLabel = GenericLabel(self.inventoryPositionFrame, text=bottomCorner)
        self.bottomCornerPositionLabel.pack(side=TOP)
        self.inventoryPositionButton = GenericButton(self.inventoryPositionFrame, text="Modifier...", command=self.select_inventory_position)
        self.inventoryPositionButton.pack(side=TOP)
        return self.frame

    def empty_inventory(self):
        loops = 0
        while(loops<60):
            loops += loops
            img = np.array(ImageGrab.grab(bbox=(self.topCornerPosition.x,self.topCornerPosition.y,self.bottomCornerPosition.x,self.bottomCornerPosition.y)))
            difference = cv2.subtract(img, self.emptyInventory)
            difference = cv2.cvtColor(difference,cv2.COLOR_BGR2GRAY)
            if np.mean(difference) == 0:
                break
            points = cv2.findNonZero(difference)
            x=points[0][0][0]
            y=points[0][0][1]
            ctypes.windll.user32.SetCursorPos(int(self.topCornerPosition.x+x+10), int(self.topCornerPosition.y+y+10))
            ctypes.windll.user32.keybd_event(0x11, 0, 0, 0) #CTRL is down
            time.sleep(0.005)
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0) # left down
            time.sleep(0.005)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0) # left up
            ctypes.windll.user32.keybd_event(0x11, 0, 0x0002, 0) #CTRL is up
            time.sleep(0.1)

    def select_inventory_position(self):
        self.inventoryPositionButton.configure(text="Haut droit dans 3...")
        self.master.update_idletasks()
        time.sleep(1)
        self.inventoryPositionButton.configure(text="Haut droit dans 2...")
        self.master.update_idletasks()
        time.sleep(1)
        self.inventoryPositionButton.configure(text="Haut droit dans 1...")
        self.master.update_idletasks()
        time.sleep(1)
        tpoint = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(tpoint))
        self.topCornerPositionLabel.configure(text="Coin haut gauche : " + str(tpoint.x)  + ", " + str(tpoint.y))
        self.inventoryPositionButton.configure(text="Bas gauche dans 3...")
        self.master.update_idletasks()
        time.sleep(1)
        self.inventoryPositionButton.configure(text="Bas gauche dans 2...")
        self.master.update_idletasks()
        time.sleep(1)
        self.inventoryPositionButton.configure(text="Bas gauche dans 1...")
        self.master.update_idletasks()
        time.sleep(1)
        bpoint = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(bpoint))
        self.bottomCornerPositionLabel.configure(text="Coin haut gauche : " + str(bpoint.x)  + ", " + str(bpoint.y))
        self.inventoryPositionButton.configure(text="Modifier...")
        self.master.update_idletasks()

        self.topCornerPosition.x = tpoint.x
        self.topCornerPosition.y = tpoint.y
        self.bottomCornerPosition.x = bpoint.x
        self.bottomCornerPosition.y = bpoint.y

        self.configProxy['pluginConfig.InventoryEmptyer.inventoryPosition.topCorner.x'] = tpoint.x
        self.configProxy['pluginConfig.InventoryEmptyer.inventoryPosition.topCorner.y'] = tpoint.y
        self.configProxy['pluginConfig.InventoryEmptyer.inventoryPosition.bottomCorner.x'] = bpoint.x
        self.configProxy['pluginConfig.InventoryEmptyer.inventoryPosition.bottomCorner.y'] = bpoint.y

        self.emptyInventory = np.array(ImageGrab.grab(bbox=(tpoint.x,tpoint.y,bpoint.x,bpoint.y)))
        cv2.imwrite(self.emptyInventoryPath, self.empty_inventory)
        with open("config.yml", 'w') as f:
            yaml.dump(self.config, f)