"""
Authentication API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserCreateOAuth, UserResponse
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    OAuthLoginRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.security import create_access_token, decode_token

router = APIRouter()


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user with email and password

    - **email**: Valid email address
    - **password**: Minimum 8 characters
    - **name**: User's display name
    - **birth_date**: Optional birth date for zodiac calculation
    - **language**: Preferred language (en, tr, de)

    Returns user data and authentication tokens
    """
    auth_service = AuthService(db)

    # Register user
    user = auth_service.register_user(user_data)

    # Generate tokens
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "tier": "free",
        }
    )

    from app.utils.security import create_refresh_token
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    return LoginResponse(
        user=UserResponse.from_orm(user),
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password

    - **email**: Registered email address
    - **password**: User password

    Returns user data and authentication tokens
    """
    auth_service = AuthService(db)

    # Login user
    user, access_token, refresh_token = auth_service.login(credentials)

    return LoginResponse(
        user=UserResponse.from_orm(user),
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/oauth", response_model=LoginResponse)
def oauth_login(
    oauth_data: OAuthLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login or register with OAuth provider (Google, Apple)

    - **provider**: "google" or "apple"
    - **id_token**: JWT token from OAuth provider

    Returns user data and authentication tokens
    """
    # TODO: Verify id_token with OAuth provider
    # For now, we'll accept it as-is (implement verification in production)

    # Extract user info from id_token
    # In production, decode and verify the id_token
    # For MVP, we'll create a simple flow

    auth_service = AuthService(db)

    # For demo purposes, create user with OAuth data
    # In production, extract from verified token
    user_data = UserCreateOAuth(
        email=f"{oauth_data.provider}@example.com",  # Extract from token
        name="OAuth User",  # Extract from token
        provider=oauth_data.provider,
        provider_id=oauth_data.id_token[:20],  # Extract from token
        language="en"
    )

    user = auth_service.register_oauth_user(user_data)

    # Generate tokens
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "tier": user.subscription.tier.value if user.subscription else "free",
        }
    )

    from app.utils.security import create_refresh_token
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    return LoginResponse(
        user=UserResponse.from_orm(user),
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token

    - **refresh_token**: Valid refresh token

    Returns new access token
    """
    # Decode refresh token
    payload = decode_token(request.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Check token type
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    # Get user
    user_id = int(payload.get("sub"))
    auth_service = AuthService(db)
    user = auth_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create new access token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "tier": user.subscription.tier.value if user.subscription else "free",
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user profile

    Requires authentication

    Returns current user data
    """
    return UserResponse.from_orm(current_user)


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user

    Note: With JWT, logout is handled client-side by deleting the token.
    This endpoint exists for consistency and can be extended with token blacklisting.

    Returns success message
    """
    # TODO: Implement token blacklisting in Redis if needed
    return {"message": "Successfully logged out"}
