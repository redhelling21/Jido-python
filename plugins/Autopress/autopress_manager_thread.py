from threading import Thread, Event
import numpy as np
import time 
import ctypes 
import cv2
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
        self.keys = {}

    def run(self): 
        
        starttime = time.time()
        msCount = 0
        while not self.stop: 
            if self.autopress.wait(1):
                for key in self.keys:
                    if int(self.keys[key][1].get()) != 0 and msCount % int(self.keys[key][1].get()) == 0:
                        print("periodic")
                        self.autopressWorkerThread.keyQueue.put(self.char2key(self.keys[key][0].get()))
                msCount += 100
                time.sleep(0.1 - ((time.time() - starttime) % 0.1))
    
    def join(self, timeout=None): 
        self.stop = True 
        super().join(timeout)

    def toggle_autopress(self):
        if (not self.autopress.is_set()):  
            print("Autopress ON")
            for key in self.keys:
                if int(self.keys[key][1].get()) == 0:
                    ctypes.windll.user32.keybd_event(self.char2key(self.keys[key][0].get()), 0, 0, 0) # Release all registered keys
            self.autopress.set()
        else:
            print("Autopress OFF")
            for key in self.keys:
                if int(self.keys[key][1].get()) == 0:
                    ctypes.windll.user32.keybd_event(self.char2key(self.keys[key][0].get()), 0, 0x0002, 0) # Release all registered keys
            self.autopress.clear()
    
    def toggle_macro(self, toggle):
        self.toggleMacro = toggle
        if not self.toggleMacro:
           self.autopress.clear()
        for key in self.keys:
            ctypes.windll.user32.keybd_event(self.char2key(self.keys[key][0].get()), 0, 0x0002, 0) # Release all registered keys

    def char2key(self, c):
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646329(v=vs.85).aspx
        result = ctypes.windll.User32.VkKeyScanW(ord(c))
        shift_state = (result & 0xFF00) >> 8
        vk_key = result & 0xFF
        return vk_key