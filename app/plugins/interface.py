
# app/plugins/interface.py

from abc import ABC, abstractmethod

class PluginInterface(ABC):
    @abstractmethod
    def initialize(self):
        """Initialize the plugin."""
        pass
pass
    @abstractmethod
    def execute(self, data):
        """Execute the plugin's main functionality."""
        pass

    @abstractmethod
    def shutdown(self):
        """Clean up resources before shutting down the plugin."""
        pass
