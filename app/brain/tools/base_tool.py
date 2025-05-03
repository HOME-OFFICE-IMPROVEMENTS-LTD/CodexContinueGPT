# app/brain/tools/base_tool.py

from abc import ABC, abstractmethod
from typing import Any

class BaseTool(ABC):
    """
    Abstract base class for all tools (plugins) that CodexContinueGPT can use.
    """

    name: str
    description: str

    @abstractmethod
    def run(self, input: str, context: dict[str, Any] = {}) -> str:
        """
        Execute the tool with a given input string and optional context.
        """
        pass
