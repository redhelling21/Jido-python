import glob
import importlib
import yaml
import sys
import os
from core.plugin_info import PluginInfos

class PluginManager():
    
    availablePlugins = {}
    loadedPlugins = {}

    def __init__(self, config):
        for pluginFolder in glob.glob('plugins/*', recursive=True):
            with open(pluginFolder+"\\plugin_info.yml", "r") as yamlInfos:
                infos = yaml.safe_load(yamlInfos)
                yamlInfos.close()
            pluginInfos = PluginInfos()
            pluginInfos.pluginPath = pluginFolder.replace("\\", ".") + ".plugin"
            pluginInfos.pluginName = infos['name']
            pluginInfos.pluginDescription = infos['description']
            pluginInfos.pluginVersion = infos['version']
            pluginInfos.isLoaded = False
            self.availablePlugins[pluginInfos.pluginName] = pluginInfos
        for pluginToLoad in config['pluginsToLoad'] :
            self.loadedPlugins[pluginToLoad] = importlib.import_module(self.availablePlugins[pluginToLoad].pluginPath).Plugin(self)
            self.availablePlugins[pluginToLoad].isLoaded = True
        if not ('General' in self.availablePlugins):
            self.loadedPlugins['General'] = importlib.import_module('plugins.General.plugin').Plugin()
            self.availablePlugins['General'].isLoaded = True


    def get_available_plugins(self):
        return self.availablePlugins
    
    def get_loaded_plugins(self):
        return self.loadedPlugins

    def load_plugins(self, plugins):
        with open("config.yml", "r") as configYaml:
            config = yaml.safe_load(configYaml)
            configYaml.close()
        config['pluginsToLoad'] = plugins
        with open("config.yml", "w") as configYaml:
            yaml.safe_dump(config, configYaml, default_flow_style=False)
            configYaml.close()
        self.restart_program()

    def restart_program():
        os.execv(sys.argv[0], sys.argv)