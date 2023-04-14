from tkinter import TOP, Canvas, Label, Toplevel
from PIL import Image, ImageTk

from gui.constants import *

def hud(pluginManager, *args, **kwargs):
    Hud(pluginManager, *args, **kwargs)

class Hud(Toplevel):
    def __init__(self, pluginManager, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.title("HUD")
        self.geometry("400x100")
        self.overrideredirect(True)
        self.attributes('-topmost', 1)
        #self.attributes('-alpha',0.5)
        self.attributes('-transparentcolor', 'grey15')
        self.config(background='grey15')
        self.canvas = Canvas(self, width=400, height=50, background=self["bg"], bd=0, highlightthickness=0)
        self.round_rectangle(0, 0, 400, 50, radius=55, fill=SIDE_MENU_BG)
        self.round_rectangle(2, 2, 398, 48, radius=55, fill='#c1dadc')
        
        self.canvas.pack(side=TOP)
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
    
    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        return self.canvas.create_polygon(points, **kwargs, smooth=True, splinesteps=64)