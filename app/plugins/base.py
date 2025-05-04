# app/plugins/base.py

from abc import ABC, abstractmethod

class CodexTool(ABC):
    name: str = "unnamed_tool"
    description: str = "No description provided"

    @abstractmethod
    def initialize(self):
        """Initialize the tool."""
        pass

    @abstractmethod
    def execute(self, input_text: str) -> dict:
        """Run the tool with the provided input."""
        pass

    @abstractmethod
    def run(self, input_text: str) -> dict:
        """Alias for execute. Override if needed."""
        pass

    @abstractmethod
    def shutdown(self):
        """Cleanup before shutdown."""
        pass

