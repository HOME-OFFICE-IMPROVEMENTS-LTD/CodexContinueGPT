# app/brain/core/base.py

from abc import ABC, abstractmethod
from typing import List, Dict

class BaseMemoryBrain(ABC):
    """
    Abstract interface for all memory brain implementations.
    """

    @abstractmethod
    def add_message(self, session_id: str, role: str, message: str) -> None:
        """Add a message to a session."""
        pass

    @abstractmethod
    def get_messages(self, session_id: str) -> List[Dict[str, str]]:
        """Retrieve the message history for a session."""
        pass

    @abstractmethod
    def clear_session(self, session_id: str) -> None:
        """Clear all messages from a session."""
        pass

    @abstractmethod
    def list_sessions(self) -> List[str]:
        """List all active session IDs."""
        pass
