# app/models/chat_models.py

from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(default="default", description="Session ID for memory tracking")
    messages: List[Message] = Field(..., description="List of chat messages")
    model: Optional[str] = Field(default="gpt-3.5-turbo", description="LLM model to use")
    provider: Optional[str] = Field(default="openai", description="Provider: openai, azure, ollama")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.0)
    tools: Optional[List[str]] = Field(default=[], description="Optional tools or plugins to use")

class ChatResponse(BaseModel):
    reply: str
    model_used: str
    tokens_used: Optional[int] = None
