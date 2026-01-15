"""
Pydantic schemas for Authentication
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.schemas.user import UserResponse


# Login schemas
class LoginRequest(BaseModel):
    """Schema for email/password login"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema for login response"""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# OAuth login
class OAuthLoginRequest(BaseModel):
    """Schema for OAuth login (Google, Apple)"""
    provider: str = Field(..., pattern="^(google|apple)$")
    id_token: str  # JWT token from OAuth provider


# Token schemas
class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: str  # user_id
    email: str
    name: str
    tier: str
    exp: int  # expiration timestamp


class RefreshTokenRequest(BaseModel):
    """Schema for refreshing access token"""
    refresh_token: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"


# Password reset
class PasswordResetRequest(BaseModel):
    """Schema for requesting password reset"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for confirming password reset"""
    token: str
    new_password: str = Field(..., min_length=8)


# Change password
class ChangePasswordRequest(BaseModel):
    """Schema for changing password"""
    old_password: str
    new_password: str = Field(..., min_length=8)
