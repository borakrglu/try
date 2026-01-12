"""
Pydantic schemas for Chat
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from app.models.chat import PersonaType, MessageRole


# Chat message schemas
class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message"""
    persona: PersonaType
    message: str = Field(..., min_length=1, max_length=2000)
    related_reading_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Schema for chat message in API responses"""
    id: int
    user_id: int
    persona: PersonaType
    role: MessageRole
    content: str
    related_reading_id: Optional[int] = None
    response_time_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Chat history
class ChatHistoryResponse(BaseModel):
    """Schema for chat history"""
    messages: List[ChatMessageResponse]
    total: int
    has_more: bool


# Streaming response (for WebSocket)
class ChatStreamChunk(BaseModel):
    """Schema for streaming chat response chunks"""
    type: str = Field(..., regex="^(chunk|done|error)$")
    content: Optional[str] = None
    error: Optional[str] = None
