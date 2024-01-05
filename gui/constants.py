from pathlib import Path
from tkinter import Tk
import customtkinter

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
