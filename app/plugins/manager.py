# app/plugins/manager.py

import os
import importlib
from typing import Dict
from app.plugins.interface import PluginInterface

class PluginManager:
    def __init__(self, plugin_directory: str = 'app/plugins'):
        self.plugin_directory = plugin_directory
        self.plugins: Dict[str, PluginInterface] = {}
        self.load_plugins()

    def load_plugins(self):
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('_plugin.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                module_path = f'app.plugins.{module_name}'
                module = importlib.import_module(module_path)

                class_name = ''.join(part.title() for part in module_name.split('_'))
                plugin_class = getattr(module, class_name, None)

                if plugin_class and issubclass(plugin_class, PluginInterface):
                    self.plugins[module_name] = plugin_class()

    def execute_plugin(self, name: str, data):
        plugin = self.plugins.get(name)
        if plugin:
            plugin.initialize()
            result = plugin.execute(data)
            plugin.shutdown()
            return result
        raise ValueError(f"Plugin '{name}' not found")

    def list_plugins(self):
        return list(self.plugins.keys())

