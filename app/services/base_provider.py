# app/services/base_provider.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: List[Dict[str, Any]]) -> str:
        """
        Send a list of messages to the LLM and return the assistant's reply.
        Each message is a dict: {"role": "user"|"assistant", "content": str}
        """
        pass
