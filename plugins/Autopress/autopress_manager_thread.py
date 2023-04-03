from threading import Lock, Thread, Event
import keyboard
import numpy as np
import time 
import ctypes 
import cv2
import random
from PIL import ImageGrab
from plugins.Autopress.autopress_worker_thread import AutoPressWorkerThread

class AutoPressManagerThread(Thread):
    def __init__(self): 
        super().__init__(daemon=True) 
        self.stop = False 
        self.autopress = Event()
        self.toggleMacro = False
        self.autopressWorkerThread = AutoPressWorkerThread()
        self.autopressWorkerThread.start()
        self.clickTimer = 0
        self.lock = Lock()
        self.keys = {}
        self.msCount = 0

    def run(self): 
        starttime = time.time()
        while not self.stop: 
            if self.autopress.wait(1):
                if(self.clickTimer != 0):
                    with self.lock:
                        self.clickTimer -= 100
                    if(self.clickTimer == 0):
                        for key in self.keys:
                            if int(self.keys[key][1].get()) == 0:
                                keyboard.press(self.keys[key][0].get())
                            else :
                                self.keys[key][2] = 0
                        self.msCount = 0
                else:
                    for key in self.keys:
                        if int(self.keys[key][1].get()) != 0 and self.msCount >= self.keys[key][2]:
                            self.autopressWorkerThread.keyQueue.put(self.keys[key][0].get())
                            self.keys[key][2] += int(self.keys[key][1].get()) * random.uniform(0.9, 1.1)
                    self.msCount += 100
                time.sleep(0.1 - ((time.time() - starttime) % 0.1))
    
    def join(self, timeout=None): 
        self.stop = True 
        super().join(timeout)

    def toggle_autopress(self):
        if (not self.autopress.is_set()):  
            print("Autopress ON")
            for key in self.keys:
                if int(self.keys[key][1].get()) == 0:
                    keyboard.press(self.keys[key][0].get()) # Release all registered keys
                else :
                    self.keys[key][2] = 0
            self.msCount = 0
            self.autopress.set()
        else:
            print("Autopress OFF")
            for key in self.keys:
                if int(self.keys[key][1].get()) == 0:
                    keyboard.release(self.keys[key][0].get()) # Release all registered keys
            self.autopress.clear()
    
    def toggle_macro(self, toggle):
        self.toggleMacro = toggle
        if not self.toggleMacro:
           self.autopress.clear()
        for key in self.keys:
            keyboard.release(self.keys[key][0].get()) # Release all registered keys
    
    def reset_click_timer(self, duration):
        if (self.autopress.is_set()): 
            if (self.clickTimer ==0):
                for key in self.keys:
                    if int(self.keys[key][1].get()) == 0:
                        keyboard.release(self.keys[key][0].get()) # Release all registered keys
            with self.lock:
                self.clickTimer = duration