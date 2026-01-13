"""
User model
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class LanguageEnum(str, enum.Enum):
    """Supported languages"""
    ENGLISH = "en"
    TURKISH = "tr"
    GERMAN = "de"


class User(Base):
    """
    User model - stores user account information
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=True)
    zodiac_sign = Column(String(20), nullable=True)  # Calculated from birth_date
    language = Column(SQLEnum(LanguageEnum), default=LanguageEnum.ENGLISH, nullable=False)

    # OAuth provider IDs
    google_id = Column(String, unique=True, nullable=True, index=True)
    apple_id = Column(String, unique=True, nullable=True, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    readings = relationship("Reading", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="user", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan")
    stats = relationship("UserStats", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notification_tokens = relationship("NotificationToken", back_populates="user", cascade="all, delete-orphan")
    notification_history = relationship("NotificationHistory", back_populates="user", cascade="all, delete-orphan")
    notification_preferences = relationship("NotificationPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
