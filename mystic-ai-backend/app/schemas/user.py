"""
Pydantic schemas for User
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

from app.models.user import LanguageEnum


# Base schema with common fields
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    language: LanguageEnum = LanguageEnum.ENGLISH


# Schema for user registration
class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=100)
    birth_date: Optional[datetime] = None


# Schema for OAuth registration (no password)
class UserCreateOAuth(UserBase):
    """Schema for OAuth user creation"""
    provider: str = Field(..., pattern="^(google|apple)$")
    provider_id: str
    birth_date: Optional[datetime] = None


# Schema for user update
class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    birth_date: Optional[datetime] = None
    language: Optional[LanguageEnum] = None


# Schema for user response (what API returns)
class UserResponse(UserBase):
    """Schema for user in API responses"""
    id: int
    zodiac_sign: Optional[str] = None
    google_id: Optional[str] = None
    apple_id: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True  # Allows creating from ORM models


# Schema for user with subscription info
class UserWithSubscription(UserResponse):
    """User with subscription details"""
    is_premium: bool
    subscription_tier: str
    subscription_expires_at: Optional[datetime] = None
