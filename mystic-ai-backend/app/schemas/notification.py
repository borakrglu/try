"""
Pydantic schemas for Notifications
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

from app.models.notification import DevicePlatform, NotificationType


# Notification token schemas
class NotificationTokenCreate(BaseModel):
    """Schema for registering a device token"""
    token: str = Field(..., min_length=10, max_length=500)
    platform: DevicePlatform
    device_id: Optional[str] = Field(None, max_length=255)
    device_name: Optional[str] = Field(None, max_length=255)


class NotificationTokenResponse(BaseModel):
    """Schema for notification token in API responses"""
    id: int
    user_id: int
    token: str
    platform: DevicePlatform
    device_id: Optional[str] = None
    device_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    last_used: datetime

    class Config:
        from_attributes = True


# Notification preferences schemas
class NotificationPreferencesUpdate(BaseModel):
    """Schema for updating notification preferences"""
    daily_affirmation: Optional[bool] = None
    reading_reminder: Optional[bool] = None
    journal_reminder: Optional[bool] = None
    moon_phase: Optional[bool] = None
    streak_milestone: Optional[bool] = None
    new_feature: Optional[bool] = None
    subscription_expiry: Optional[bool] = None
    quiet_hours_enabled: Optional[bool] = None
    quiet_hours_start: Optional[str] = Field(None, regex=r"^([01]\d|2[0-3]):[0-5]\d$")
    quiet_hours_end: Optional[str] = Field(None, regex=r"^([01]\d|2[0-3]):[0-5]\d$")


class NotificationPreferencesResponse(BaseModel):
    """Schema for notification preferences in API responses"""
    id: int
    user_id: int
    daily_affirmation: bool
    reading_reminder: bool
    journal_reminder: bool
    moon_phase: bool
    streak_milestone: bool
    new_feature: bool
    subscription_expiry: bool
    quiet_hours_enabled: bool
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Notification sending schema
class NotificationSend(BaseModel):
    """Schema for sending a custom notification"""
    notification_type: NotificationType
    title: str = Field(..., min_length=1, max_length=255)
    body: str = Field(..., min_length=1, max_length=1000)
    data: Optional[Dict[str, Any]] = None


# Notification history schema
class NotificationHistoryResponse(BaseModel):
    """Schema for notification history in API responses"""
    id: int
    user_id: int
    notification_type: NotificationType
    title: str
    body: str
    data: Optional[str] = None
    sent: bool
    delivered: bool
    opened: bool
    error_message: Optional[str] = None
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None

    class Config:
        from_attributes = True
