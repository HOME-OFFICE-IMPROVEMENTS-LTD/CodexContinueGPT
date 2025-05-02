
import os
from typing import Dict
from importlib import import_module
from interface import PluginInterface

class PluginManager:
    def __init__(self, plugin_directory: str = 'app/plugins'):
        self.plugin_directory = plugin_directory
        self.plugins: Dict[str, PluginInterface] = {}
        self.load_plugins()

    def load_plugins(self):
        # Load each plugin based on the files
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('_plugin.py') and filename != 'interface.py':
                module_name = filename[:-3]
                module = import_module(f'app.plugins.{module_name}')
                plugin_class = getattr(module, module_name.title().replace('_', ''))
                if issubclass(plugin_class, PluginInterface):
                    self.plugins[module_name] = plugin_class()

    def execute_plugin(self, name: str, data):
        plugin = self.plugins.get(name)
        if plugin:
            plugin.initialize()
            result = plugin.execute(data)
            plugin.shutdown()
            return result
        else:
            raise ValueError(f"Plugin {name} not found")

    def list_plugins(self):
        return list(self.plugins.keys())
