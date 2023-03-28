import queue
from threading import Thread, Event
import unicodedata
import numpy as np
import time 
import ctypes 
import cv2
from PIL import ImageGrab

class AutoPressWorkerThread(Thread):
    def __init__(self): 
        super().__init__(daemon=True) 
        self.stop = False 
        self.keyQueue = queue.Queue()

    def run(self): 
        while not self.stop: 
            key = self.keyQueue.get()
            ctypes.windll.user32.keybd_event(key, 0, 0, 0)
            time.sleep(0.02)
            ctypes.windll.user32.keybd_event(key, 0, 0x0002, 0)
            time.sleep(0.3)
    
    def join(self, timeout=None): 
        self.stop = True 
        super().join(timeout)