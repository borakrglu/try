"""
FastAPI dependencies - Reusable dependency injection functions
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Generator

from app.db.session import get_db
from app.models.user import User
from app.utils.security import decode_token
from app.services.auth_service import AuthService


# Security scheme for JWT bearer tokens
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token

    Usage:
        @app.get("/profile")
        def get_profile(user: User = Depends(get_current_user)):
            return {"name": user.name}

    Args:
        credentials: Bearer token from Authorization header
        db: Database session

    Returns:
        Authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Decode token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user ID from token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    auth_service = AuthService(db)
    user = auth_service.get_user_by_id(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (can be extended with status checks)

    Args:
        current_user: Current authenticated user

    Returns:
        Current active user
    """
    # Can add additional checks here (e.g., is_active, is_verified)
    return current_user


def require_premium(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Require user to have premium subscription

    Usage:
        @app.get("/premium-feature")
        def premium_feature(user: User = Depends(require_premium)):
            return {"data": "premium content"}

    Args:
        current_user: Current authenticated user

    Returns:
        User with premium subscription

    Raises:
        HTTPException: If user is not premium
    """
    if not current_user.subscription.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required"
        )

    return current_user


def check_reading_limit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Check if user can make a reading (free tier: 3/month)

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User if allowed

    Raises:
        HTTPException: If limit reached
    """
    subscription = current_user.subscription

    if not subscription.can_make_reading():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Reading limit reached. You've used {subscription.readings_this_month}/3 readings this month. Upgrade to premium for unlimited readings."
        )

    return current_user


def check_chat_limit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Check if user can send chat message (free tier: 10/day)

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User if allowed

    Raises:
        HTTPException: If limit reached
    """
    subscription = current_user.subscription

    if not subscription.can_send_chat_message():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Chat limit reached. You've used {subscription.chat_messages_today}/10 messages today. Upgrade to premium for unlimited chat."
        )

    return current_user


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Require user to be an admin

    Usage:
        @app.get("/admin/users")
        def list_users(admin: User = Depends(get_admin_user)):
            return {"users": [...]}

    Args:
        current_user: Current authenticated user

    Returns:
        Admin user

    Raises:
        HTTPException: If user is not admin or is banned
    """
    if current_user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is banned: {current_user.ban_reason or 'No reason provided'}"
        )

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


async def check_not_banned(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Check if user is not banned

    Args:
        current_user: Current authenticated user

    Returns:
        User if not banned

    Raises:
        HTTPException: If user is banned
    """
    if current_user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is banned: {current_user.ban_reason or 'No reason provided'}"
        )

    return current_user
