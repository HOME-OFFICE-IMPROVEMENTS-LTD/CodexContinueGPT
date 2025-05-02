# app/brain/session_store.py

import os
import json
from typing import List, Dict

class SessionStore:
    def __init__(self, storage_path: str = "app/brain/logs"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def _get_file_path(self, session_id: str) -> str:
        return os.path.join(self.storage_path, f"{session_id}.json")

    def save(self, session_id: str, messages: List[Dict]):
        path = self._get_file_path(session_id)
        with open(path, "w") as f:
            json.dump(messages, f, indent=2)

    def load(self, session_id: str) -> List[Dict]:
        path = self._get_file_path(session_id)
        if not os.path.exists(path):
            return []
        with open(path, "r") as f:
            return json.load(f)

    def list_sessions(self) -> List[str]:
        return [f.replace(".json", "") for f in os.listdir(self.storage_path) if f.endswith(".json")]

    def clear(self, session_id: str):
        path = self._get_file_path(session_id)
        if os.path.exists(path):
            os.remove(path)
