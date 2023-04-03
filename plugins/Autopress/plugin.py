import pathlib
import time

import PIL
from core.plugin_core import PluginCore
from tkinter import BOTTOM, LEFT, Entry, Frame, Label, TOP, PhotoImage, StringVar, ttk
import customtkinter
from core.plugin_manager import PluginManager
from gui.components.generic_button import GenericButton
from gui.components.generic_checkbox import GenericCheckBox
from gui.components.generic_entry import GenericEntry
from gui.components.generic_label import GenericLabel
from gui.components.hotkey_frame import HotKeyFrame
import gui.main_window as mainwindow
from PIL import Image
from plugins.Autopress.autopress_manager_thread import AutoPressManagerThread
from gui.components.title_frame import TitleFrame
import keyboard
import mouse
import yaml
from scalpl import Cut
import uuid

class Plugin(PluginCore):
    def __init__(self, config):
        self.config=config
        self.toggleMacro = False
        self.configProxy=Cut(config)
        self.autopressThread = AutoPressManagerThread()
        self.keys = {}
        self.keysFrames = {}
        keyboard.on_press_key(self.configProxy['pluginConfig.Autopress.hotkey'], self.toggle_autopress)
        self.clickHandler = mouse.on_click(self.click_during_pause)
        self.currentClicks = 0
        self.autopressThread.start()

    def get_frame(self, master):
        self.master = master
        self.frame = Frame(master)
        self.clickOnPauseDelay = StringVar(self.frame, self.configProxy.get('pluginConfig.Autopress.clickOnPause.delay', '1200'))
        self.clickOnPauseToggle = StringVar(self.frame, self.configProxy.get('pluginConfig.Autopress.clickOnPause.activated', '0'))
        self.titleFrame = TitleFrame(self.frame, 'Autopress')
        self.titleFrame.pack(side=TOP, fill="x", expand=True)
        labelString = """
        Appuie automatiquement sur les touches demandées.
        Si deux touches entrent en conflit, elles sont pressées dans l'ordre de la liste.
        Ne renseigner que des délais multiples de 100ms (0 = constant).
        """
        self.descriptionLabel = GenericLabel(self.frame, text=labelString)
        self.descriptionLabel.pack(side=TOP)
        self.hotKeyFrame = HotKeyFrame(self.frame, 'pluginConfig.Autopress.hotkey', "Activer l'autopress :", self.toggle_autopress, self.config, True)
        self.hotKeyFrame.pack(side=TOP)
        self.pauseOnClickFrame = Frame (self.frame, background=mainwindow.MAIN_BG, pady=10)
        self.pauseOnClickLabel = GenericLabel(self.pauseOnClickFrame, text='Pause lors d\'un clic : ')
        self.pauseOnClickEntry = GenericEntry(self.pauseOnClickFrame, textvariable=self.clickOnPauseDelay)
        self.pauseOnClickMsLabel = GenericLabel(self.pauseOnClickFrame, text='ms')
        self.pauseOnClickCheckBox = GenericCheckBox(self.pauseOnClickFrame, text="Activer", variable=self.clickOnPauseToggle)
        self.pauseOnClickLabel.pack(side=LEFT)
        self.pauseOnClickEntry.pack(side=LEFT)
        self.pauseOnClickMsLabel.pack(side=LEFT)
        self.pauseOnClickCheckBox.pack(side=LEFT, padx=10)
        self.pauseOnClickFrame.pack(side=TOP)
        self.keysToPressFrame = Frame(self.frame, background=mainwindow.MAIN_BG, pady=10, highlightthickness=1, highlightbackground="grey")
        self.keysToPressFrame.pack(side=TOP)
        self.addKeysToPressButton = GenericButton(self.frame, text="Ajouter une touche", command=self.add_key_to_press)
        self.addKeysToPressButton.pack(side=TOP, pady=15)
        self.saveKeysButton = GenericButton(self.frame, text="Sauver", command=self.save_config)
        self.saveKeysButton.pack(side=TOP, pady=15)
        for key in self.configProxy.get('pluginConfig.Autopress.keys', ''):
            self.add_key_to_press(key=key['key'], delay=key['key_delay'])
        self.autopressThread.keys = self.keys
        return self.frame

    def toggle_autopress(self, truc):
        if self.toggleMacro:
            self.autopressThread.toggle_autopress()
    
    def toggle_macro(self, toggle):
        self.toggleMacro = toggle
        self.autopressThread.toggle_macro(toggle)

    def add_key_to_press(self, key='', delay=''):
        id = uuid.uuid4().hex
        self.keys[id] = [StringVar(self.frame, key), StringVar(self.frame, delay), 0]
        frame = Frame(self.keysToPressFrame, name=id, background=mainwindow.MAIN_BG, pady=2)
        labelKey = GenericLabel(frame, text='Touche')
        entryKey = GenericEntry(frame, textvariable=self.keys[id][0], width = 70)
        labelDelay = GenericLabel(frame, text='Délai')
        entryDelay = GenericEntry(frame, textvariable=self.keys[id][1], width = 100)
        labelMs = GenericLabel(frame, text='ms')
        buttonDelete = GenericButton(frame, text="-", width=30, height=15, command= lambda: self.delete_key_to_press(id))
        labelKey.pack(side=LEFT)
        entryKey.pack(side=LEFT)
        labelDelay.pack(side=LEFT, padx=(10, 0))
        entryDelay.pack(side=LEFT)
        labelMs.pack(side=LEFT, padx=(0, 10))
        buttonDelete.pack(side=LEFT)
        frame.pack(side=TOP, padx=60)
        self.keysFrames[id] = frame
    
    def delete_key_to_press(self, id):
        self.keys.pop(id)
        self.keysFrames[id].pack_forget()
        self.keysFrames[id].destroy()
        self.keysFrames.pop(id)

    def save_config(self):
        self.autopressThread.keys = self.keys
        tempKeyDict = []
        for key in self.keys:
            tempKeyDict.append({'key':self.keys[key][0].get(), 'key_delay': int(self.keys[key][1].get())}) 
        self.configProxy['pluginConfig.Autopress.keys'] = tempKeyDict
        self.configProxy['pluginConfig.Autopress.clickOnPause'] = {'activated': int(self.clickOnPauseToggle.get()), 'delay': int(self.clickOnPauseDelay.get())}
        with open("config.yml", 'w') as f:
            yaml.dump(self.config, f)

    def click_during_pause(self):
        if int(self.clickOnPauseToggle.get()) == 1:
            self.autopressThread.reset_click_timer(int(self.clickOnPauseDelay.get()))