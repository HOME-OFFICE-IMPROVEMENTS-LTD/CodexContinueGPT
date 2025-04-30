# app/brain/core/base.py

from abc import ABC, abstractmethod
from typing import List, Dict

class CodexTool(ABC):
    """Abstract base for all tools/plugins used by CodexContinueGPT."""

    @abstractmethod
    async def run(self, prompt: str, session_id: str) -> str:
        """Execute the tool logic and return output."""
        pass

class CodexResponse:
    """A structured response returned by the brain kernel."""

    def __init__(self, reply: str, thoughts: Dict = None):
        self.reply = reply
        self.thoughts = thoughts or {}
