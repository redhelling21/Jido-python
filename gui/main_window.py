from pathlib import Path
from tkinter import *
from tkinter import ttk
import customtkinter
from ctypes import windll
import ctypes
import PIL as pil
from gui.components.menu_button import MenuButton
from gui.general_frame import *

#   shortcuts to the WinAPI functionality
set_window_pos = ctypes.windll.user32.SetWindowPos
set_window_long = ctypes.windll.user32.SetWindowLongPtrW
get_window_long = ctypes.windll.user32.GetWindowLongPtrW
get_parent = ctypes.windll.user32.GetParent

#   some of the WinAPI flags
GWL_STYLE = -16

WS_OVERLAPPED = 0x00000000
WS_CAPTION = 0x00C00000
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_THICKFRAME = 0x00040000
WS_SYSMENU = 0x00080000

SWP_NOZORDER = 4
SWP_NOMOVE = 2
SWP_NOSIZE = 1
SWP_FRAMECHANGED = 32

root = Tk()  # Make temporary window for app to start
root.withdraw()
ASSET_PATH = Path(__file__).parent / Path("./assets")
SIDE_MENU_BG = "#4d8388"
SIDE_MENU_BG_ACTIVE = "#45757a"
SIDE_MENU_BG_ACTIVE_HOVER = "#5e8f93"
MAIN_BG = "#FFFFFF"
SIDEBAR_SIZE = 260
FONT_MENU = customtkinter.CTkFont(family="Inter V Medium", size=15)
FONT_TITLE = customtkinter.CTkFont(family="Inter", size=30)
FONT_COMPONENT = customtkinter.CTkFont(family="Inter V Medium", size=12)
FONT_GENERAL = customtkinter.CTkFont(family="Inter V Medium", size=13)
FONT_TABLE = customtkinter.CTkFont(family="Inter V Medium", size=12)
FONT_TABLE_HEADING = customtkinter.CTkFont(family="Inter V Medium", size=14)

def mainWindow(config, pluginManager, *args, **kwargs):
    MainWindow(config, pluginManager, *args, **kwargs)

class MainWindow(Toplevel):

    activeMenu = 'Général'
    menuButtons = {}
    pluginFrames = {}

    def __init__(self, config, pluginManager, *args, **kwargs):
        self.loadedPlugins = pluginManager.get_loaded_plugins()
        Toplevel.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.title("JIDO - No more pain while playing !")
        self.geometry("1080x640")
        self.attributes('-transparentcolor', 'grey15')
        self.config(background='grey15')

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=True)

        #region Sidebar

        self.sidebar = Frame(self.canvas, width=SIDEBAR_SIZE, background=SIDE_MENU_BG)
        self.sidebar.pack_propagate(False)
        self.sidebar.pack(fill=Y, side=LEFT)
        

        self.logoFrame = Frame(self.sidebar, width=SIDEBAR_SIZE, background=SIDE_MENU_BG, padx=20, pady=20)
        self.logoFrame.pack(side=TOP)

        logo_image  = PhotoImage(file=ASSET_PATH/"logo.png")
        label = Label(self.logoFrame, image = logo_image, background=SIDE_MENU_BG)
        label.pack()
        separator = ttk.Separator(self.logoFrame, orient='horizontal')
        separator.pack(fill=X, pady=20)

        self.menuFrame = Frame(self.sidebar, width=SIDEBAR_SIZE, background=SIDE_MENU_BG, padx=15)
        self.menuFrame.pack(fill=Y, side=TOP, expand=True)

        #region Default buttons

        general_img = customtkinter.CTkImage(pil.Image.open("gui/assets/general_icon.png"))
        general_btn = MenuButton(
            self.menuFrame,
            image=general_img,
            command=lambda : self.handle_menu('Général'),
            text='Général'
        )
        self.menuButtons['Général'] = general_btn
        general_btn.configure(fg_color=SIDE_MENU_BG_ACTIVE)
        general_btn.pack(side=TOP, pady=2)

        #endregion

        #region Plugins buttons

        for pluginName, plugin in self.loadedPlugins.items():
            img = customtkinter.CTkImage(pil.Image.open("plugins/"+pluginName+"/icon.png"))
            btn = MenuButton(
                self.menuFrame,
                image=img,
                command=lambda i=pluginName: self.handle_menu(i),
                text=pluginName
            )
            self.menuButtons[pluginName] = btn
            btn.configure(fg_color='transparent')
            btn.pack(side=TOP, pady=2)

        #endregion
        #endregion
        #region Mainframe

        self.mainCanvas = Canvas(self.canvas, background=MAIN_BG, highlightthickness=0)
        self.mainCanvas.pack(fill=BOTH, side=LEFT, expand=True)
        self.mainCanvas.bind('<Configure>', self.main_canvas_width)
        
        self.mainScrollableFrame = Frame(self.mainCanvas, background=MAIN_BG)
        self.mainScrollableFrame.pack(fill=BOTH, side=TOP, expand=True)

        self.mainScrollableFrame.bind('<Enter>', self._bound_to_mousewheel)
        self.mainScrollableFrame.bind('<Leave>', self._unbound_to_mousewheel)
        self.mainScrollableFrame.bind("<Configure>", lambda e: self.mainCanvas.configure(scrollregion=self.mainCanvas.bbox("all")))

        self.mainCanvasFrame = self.mainCanvas.create_window((0, 0), window=self.mainScrollableFrame, anchor="nw")

        self.pluginFrames['Général'] = GeneralFrame(config=config, master=self.mainScrollableFrame, pluginmanager=pluginManager)
        for pluginName, plugin in self.loadedPlugins.items():
            self.pluginFrames[pluginName] = self.loadedPlugins[pluginName].get_frame(self.mainScrollableFrame)
        
        self.mainFrame = self.pluginFrames['Général']
        self.mainFrame.configure(background=MAIN_BG)
        self.mainFrame.pack(fill=BOTH, side=LEFT, expand=True),
        
        
        #endregion

        self.resizable(True, True)
        self.mainloop()

    def close_window(self):
        self.quit() 
        self.destroy()
        
    def handle_menu(self, menuItemName):
        if self.activeMenu == menuItemName:
            return
        self.menuButtons[menuItemName].configure(fg_color=SIDE_MENU_BG_ACTIVE, hover_color=SIDE_MENU_BG_ACTIVE)
        self.menuButtons[self.activeMenu].configure(fg_color='transparent', hover_color=SIDE_MENU_BG_ACTIVE_HOVER)
        self.activeMenu = menuItemName
        self.mainFrame.pack_forget()
        self.mainFrame = self.pluginFrames[menuItemName]
        self.mainFrame.configure(background=MAIN_BG)
        self.mainFrame.pack(fill=BOTH, side=LEFT, expand=True)

    def _bound_to_mousewheel(self, event):
        self.mainCanvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.mainCanvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.mainCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def main_canvas_width(self, event):
        canvas_width = event.width
        self.mainCanvas.itemconfig(self.mainCanvasFrame, width = canvas_width)