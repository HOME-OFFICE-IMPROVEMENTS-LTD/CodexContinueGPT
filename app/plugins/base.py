# app/plugins/base.py

from abc import ABC, abstractmethod

class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    async def run(self, input_text: str) -> str:
        pass
