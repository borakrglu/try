"""
Webhook Schemas - Pydantic models for webhook payloads
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class RevenueCatEventType(str, Enum):
    """RevenueCat webhook event types"""
    INITIAL_PURCHASE = "INITIAL_PURCHASE"
    RENEWAL = "RENEWAL"
    CANCELLATION = "CANCELLATION"
    UNCANCELLATION = "UNCANCELLATION"
    NON_RENEWING_PURCHASE = "NON_RENEWING_PURCHASE"
    EXPIRATION = "EXPIRATION"
    BILLING_ISSUE = "BILLING_ISSUE"
    PRODUCT_CHANGE = "PRODUCT_CHANGE"
    TRANSFER = "TRANSFER"
    SUBSCRIPTION_PAUSED = "SUBSCRIPTION_PAUSED"
    SUBSCRIPTION_EXTENDED = "SUBSCRIPTION_EXTENDED"


class RevenueCatSubscriber(BaseModel):
    """RevenueCat subscriber information"""
    original_app_user_id: str
    first_seen: datetime
    last_seen: datetime
    entitlements: Dict[str, Any] = {}
    subscriptions: Dict[str, Any] = {}


class RevenueCatEvent(BaseModel):
    """RevenueCat webhook event payload"""
    api_version: str = "1.0"
    event: RevenueCatEventType
    app_id: str
    app_user_id: str
    original_app_user_id: str

    # Product information
    product_id: Optional[str] = None
    period_type: Optional[str] = None  # 'TRIAL', 'INTRO', 'NORMAL'

    # Purchase information
    purchased_at_ms: Optional[int] = None
    expiration_at_ms: Optional[int] = None

    # Store information
    store: Optional[str] = None  # 'APP_STORE', 'PLAY_STORE', 'STRIPE', etc.
    environment: Optional[str] = None  # 'PRODUCTION', 'SANDBOX'

    # Transaction details
    price: Optional[float] = None
    currency: Optional[str] = None

    # Subscriber data (nested object)
    subscriber_attributes: Optional[Dict[str, Any]] = None


class WebhookResponse(BaseModel):
    """Standard webhook response"""
    success: bool
    message: str
    event_id: Optional[str] = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)


class WebhookEventResponse(BaseModel):
    """Webhook event database record response"""
    id: int
    source: str
    event_type: str
    event_id: Optional[str]
    user_id: Optional[int]
    processed: bool
    processed_at: Optional[datetime]
    error_message: Optional[str]
    received_at: datetime

    class Config:
        from_attributes = True
