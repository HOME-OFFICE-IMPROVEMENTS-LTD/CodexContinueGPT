# app/models/chat_models.py

from pydantic import BaseModel, Field
from typing import Optional, Literal

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(default=None, description="Session ID")
    message: str = Field(..., description="User's input prompt")
    provider: Optional[Literal["openai", "azure", "ollama"]] = Field(
        default="openai", description="LLM provider selection"
    )
    memory: Optional[bool] = Field(default=True, description="Enable memory or stateless mode")
