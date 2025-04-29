# app/brain/memory_interface.py

from abc import ABC, abstractmethod
from app.brain.agent_schema import AgentMessage
from typing import List

class MemoryInterface(ABC):

    @abstractmethod
    def add(self, message: AgentMessage) -> None:
        ...

    @abstractmethod
    def get(self, session_id: str) -> List[AgentMessage]:
        ...

    @abstractmethod
    def clear(self, session_id: str) -> None:
        ...
