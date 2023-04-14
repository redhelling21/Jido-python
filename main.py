import tkinter as tk
import yaml
from core.plugin_manager import PluginManager
from gui.hud import hud
from gui.main_window import mainWindow


# Main window constructor
root = tk.Tk()  # Make temporary window for app to start
root.withdraw()

with open("config.yml", "r") as configYaml:
    config = yaml.safe_load(configYaml)
    configYaml.close()

pluginManager = PluginManager(config)

if __name__ == "__main__":
    mainWindow(config, pluginManager)
