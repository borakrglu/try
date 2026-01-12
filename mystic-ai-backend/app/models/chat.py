"""
Chat message model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class PersonaType(str, enum.Enum):
    """Available chat personas"""
    SAGE = "sage"
    WITCH = "witch"
    ASTROLOGER = "astrologer"


class MessageRole(str, enum.Enum):
    """Message role in conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(Base):
    """
    Chat message model - stores conversation history
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Persona used for this conversation
    persona = Column(SQLEnum(PersonaType), nullable=False, index=True)

    # Message role (user, assistant, system)
    role = Column(SQLEnum(MessageRole), nullable=False)

    # Message content
    content = Column(Text, nullable=False)

    # Optional: Reference to related reading
    related_reading_id = Column(Integer, ForeignKey("readings.id"), nullable=True)

    # Performance metrics
    response_time_ms = Column(Integer, nullable=True)  # Time to generate response
    tokens_used = Column(Integer, nullable=True)  # API tokens consumed

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="chat_messages")

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, user_id={self.user_id}, persona={self.persona}, role={self.role})>"
