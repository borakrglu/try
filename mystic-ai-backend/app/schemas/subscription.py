"""
Pydantic schemas for Subscriptions
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.models.subscription import SubscriptionTier, SubscriptionStatus, PlatformType


# Receipt verification schemas
class ReceiptVerifyRequest(BaseModel):
    """Schema for verifying App Store / Play Store receipt"""
    platform: PlatformType
    receipt_data: str  # Base64 encoded receipt


class SubscriptionResponse(BaseModel):
    """Schema for subscription in API responses"""
    id: int
    user_id: int
    tier: SubscriptionTier
    status: SubscriptionStatus
    platform: Optional[PlatformType] = None
    started_at: datetime
    expires_at: Optional[datetime] = None
    trial_ends_at: Optional[datetime] = None
    auto_renew: bool
    is_premium: bool
    is_trial: bool

    class Config:
        from_attributes = True


# Usage status
class UsageStatusResponse(BaseModel):
    """Schema for subscription usage status"""
    tier: SubscriptionTier
    status: SubscriptionStatus
    is_premium: bool
    readings_this_month: int
    readings_limit: int
    chat_messages_today: int
    chat_messages_limit: int
    can_make_reading: bool
    can_send_chat_message: bool
    expires_at: Optional[datetime] = None


# Subscription management
class SubscriptionCancelRequest(BaseModel):
    """Schema for canceling subscription"""
    reason: Optional[str] = Field(None, max_length=500)


# Webhook from RevenueCat
class RevenueCatWebhook(BaseModel):
    """Schema for RevenueCat webhook events"""
    type: str  # INITIAL_PURCHASE, RENEWAL, CANCELLATION, etc.
    app_user_id: str
    product_id: str
    purchased_at_ms: int
    expiration_at_ms: Optional[int] = None
    is_trial: bool = False
