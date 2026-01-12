"""
Subscription model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class SubscriptionTier(str, enum.Enum):
    """Subscription tiers"""
    FREE = "free"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ANNUAL = "annual"


class SubscriptionStatus(str, enum.Enum):
    """Subscription status"""
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"
    TRIAL = "trial"


class PlatformType(str, enum.Enum):
    """Purchase platform"""
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


class Subscription(Base):
    """
    Subscription model - stores user subscription information
    """
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)

    # Subscription tier and status
    tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False, index=True)

    # Platform (iOS, Android, Web)
    platform = Column(SQLEnum(PlatformType), nullable=True)

    # Store receipt/transaction data
    original_transaction_id = Column(String, unique=True, nullable=True, index=True)
    latest_receipt = Column(String, nullable=True)  # Base64 encoded receipt

    # Product ID from App Store / Play Store
    product_id = Column(String, nullable=True)

    # Subscription dates
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    trial_ends_at = Column(DateTime, nullable=True)

    # Auto-renewal
    auto_renew = Column(Boolean, default=True, nullable=False)

    # Usage tracking (for free tier limits)
    readings_this_month = Column(Integer, default=0, nullable=False)
    chat_messages_today = Column(Integer, default=0, nullable=False)
    last_usage_reset = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    user = relationship("User", back_populates="subscription")

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, tier={self.tier}, status={self.status})>"

    @property
    def is_premium(self) -> bool:
        """Check if user has active premium subscription"""
        if self.status != SubscriptionStatus.ACTIVE:
            return False
        if self.tier == SubscriptionTier.FREE:
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        return True

    @property
    def is_trial(self) -> bool:
        """Check if subscription is in trial period"""
        if self.status != SubscriptionStatus.TRIAL:
            return False
        if self.trial_ends_at and self.trial_ends_at < datetime.utcnow():
            return False
        return True

    def can_make_reading(self) -> bool:
        """Check if user can make a reading (free tier limit: 3/month)"""
        if self.is_premium or self.is_trial:
            return True
        return self.readings_this_month < 3

    def can_send_chat_message(self) -> bool:
        """Check if user can send chat message (free tier limit: 10/day)"""
        if self.is_premium or self.is_trial:
            return True
        return self.chat_messages_today < 10
