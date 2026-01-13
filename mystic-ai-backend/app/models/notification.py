"""
Notification models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class DevicePlatform(str, enum.Enum):
    """Device platform types"""
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


class NotificationType(str, enum.Enum):
    """Notification types"""
    DAILY_AFFIRMATION = "daily_affirmation"
    READING_REMINDER = "reading_reminder"
    JOURNAL_REMINDER = "journal_reminder"
    MOON_PHASE = "moon_phase"
    STREAK_MILESTONE = "streak_milestone"
    NEW_FEATURE = "new_feature"
    SUBSCRIPTION_EXPIRY = "subscription_expiry"
    CUSTOM = "custom"


class NotificationToken(Base):
    """
    Device notification token model - stores FCM tokens for push notifications
    """
    __tablename__ = "notification_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # FCM token
    token = Column(String, nullable=False, unique=True, index=True)

    # Device info
    platform = Column(SQLEnum(DevicePlatform), nullable=False)
    device_id = Column(String, nullable=True)
    device_name = Column(String, nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_used = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    user = relationship("User", back_populates="notification_tokens")

    def __repr__(self):
        return f"<NotificationToken(id={self.id}, user_id={self.user_id}, platform={self.platform})>"


class NotificationHistory(Base):
    """
    Notification history model - tracks all sent notifications
    """
    __tablename__ = "notification_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Notification details
    notification_type = Column(SQLEnum(NotificationType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    data = Column(Text, nullable=True)  # JSON string for additional data

    # Status
    sent = Column(Boolean, default=False, nullable=False)
    delivered = Column(Boolean, default=False, nullable=False)
    opened = Column(Boolean, default=False, nullable=False)
    error_message = Column(String(500), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)

    # Relationship
    user = relationship("User", back_populates="notification_history")

    def __repr__(self):
        return f"<NotificationHistory(id={self.id}, type={self.notification_type}, sent={self.sent})>"


class NotificationPreferences(Base):
    """
    User notification preferences - opt-in/opt-out settings
    """
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)

    # Notification type preferences (all default to True)
    daily_affirmation = Column(Boolean, default=True, nullable=False)
    reading_reminder = Column(Boolean, default=True, nullable=False)
    journal_reminder = Column(Boolean, default=True, nullable=False)
    moon_phase = Column(Boolean, default=True, nullable=False)
    streak_milestone = Column(Boolean, default=True, nullable=False)
    new_feature = Column(Boolean, default=True, nullable=False)
    subscription_expiry = Column(Boolean, default=True, nullable=False)

    # Quiet hours (24-hour format, e.g., "22:00-08:00")
    quiet_hours_enabled = Column(Boolean, default=False, nullable=False)
    quiet_hours_start = Column(String(5), nullable=True)  # e.g., "22:00"
    quiet_hours_end = Column(String(5), nullable=True)    # e.g., "08:00"

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    user = relationship("User", back_populates="notification_preferences")

    def __repr__(self):
        return f"<NotificationPreferences(user_id={self.user_id})>"
