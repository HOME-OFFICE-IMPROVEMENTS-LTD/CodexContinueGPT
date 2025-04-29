# app/brain/agent_schema.py

from pydantic import BaseModel, Field
from typing import Literal, Optional

class AgentMetadata(BaseModel):
    id: str
    role: Literal["user", "assistant", "system"]
    name: Optional[str] = "Anonymous"
    model: Optional[str] = None
    memory_scope: Optional[str] = Field(default="session", description="session, project, or global")
    active: bool = True

class AgentMessage(BaseModel):
    session_id: str
    sender: AgentMetadata
    content: str
    timestamp: Optional[str] = None
