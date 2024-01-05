import queue
from threading import Thread
import keyboard
import time


class AutoPressWorkerThread(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.stop = False
        self.keyQueue = queue.Queue()

    def run(self):
        while not self.stop:
            key = self.keyQueue.get()
            keyboard.press(key)
            time.sleep(0.1)
            keyboard.release(key)
            time.sleep(0.3)

    def join(self, timeout=None):
        self.stop = True
        super().join(timeout)
