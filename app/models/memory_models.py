# app/models/memory_models.py

from pydantic import BaseModel

class ClearMemoryRequest(BaseModel):
    session_id: str
