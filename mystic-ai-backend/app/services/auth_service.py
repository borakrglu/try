"""
Authentication service - Business logic for auth operations
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional, Tuple

from app.models.user import User
from app.models.subscription import Subscription, SubscriptionTier, SubscriptionStatus
from app.models.user_stats import UserStats
from app.schemas.user import UserCreate, UserCreateOAuth
from app.schemas.auth import LoginRequest, LoginResponse, OAuthLoginRequest
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.utils.zodiac import calculate_zodiac_sign


class AuthService:
    """Authentication service"""

    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: UserCreate) -> User:
        """
        Register a new user with email/password

        Args:
            user_data: User registration data

        Returns:
            Created user

        Raises:
            HTTPException: If email already exists
        """
        # Check if email exists
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Calculate zodiac sign if birth date provided
        zodiac_sign = None
        if user_data.birth_date:
            zodiac_sign = calculate_zodiac_sign(user_data.birth_date)

        # Create user
        user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            name=user_data.name,
            birth_date=user_data.birth_date,
            zodiac_sign=zodiac_sign,
            language=user_data.language,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # Create free subscription
        self._create_free_subscription(user.id)

        # Create user stats (for gamification)
        self._create_user_stats(user.id)

        return user

    def register_oauth_user(self, oauth_data: UserCreateOAuth) -> User:
        """
        Register a new user via OAuth (Google, Apple)

        Args:
            oauth_data: OAuth user data

        Returns:
            Created or existing user
        """
        # Check if user exists with this OAuth provider
        if oauth_data.provider == "google":
            existing_user = self.db.query(User).filter(
                User.google_id == oauth_data.provider_id
            ).first()
        elif oauth_data.provider == "apple":
            existing_user = self.db.query(User).filter(
                User.apple_id == oauth_data.provider_id
            ).first()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OAuth provider"
            )

        if existing_user:
            # Update last login
            existing_user.last_login = datetime.utcnow()
            self.db.commit()
            return existing_user

        # Check if email exists (user may have registered with email first)
        user_with_email = self.db.query(User).filter(User.email == oauth_data.email).first()
        if user_with_email:
            # Link OAuth provider to existing account
            if oauth_data.provider == "google":
                user_with_email.google_id = oauth_data.provider_id
            elif oauth_data.provider == "apple":
                user_with_email.apple_id = oauth_data.provider_id

            user_with_email.last_login = datetime.utcnow()
            self.db.commit()
            return user_with_email

        # Create new user
        zodiac_sign = None
        if oauth_data.birth_date:
            zodiac_sign = calculate_zodiac_sign(oauth_data.birth_date)

        user = User(
            email=oauth_data.email,
            name=oauth_data.name,
            birth_date=oauth_data.birth_date,
            zodiac_sign=zodiac_sign,
            language=oauth_data.language,
            google_id=oauth_data.provider_id if oauth_data.provider == "google" else None,
            apple_id=oauth_data.provider_id if oauth_data.provider == "apple" else None,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # Create free subscription
        self._create_free_subscription(user.id)

        # Create user stats
        self._create_user_stats(user.id)

        return user

    def login(self, credentials: LoginRequest) -> Tuple[User, str, str]:
        """
        Login with email/password

        Args:
            credentials: Login credentials

        Returns:
            Tuple of (user, access_token, refresh_token)

        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email
        user = self.db.query(User).filter(User.email == credentials.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Check if user has password (OAuth users may not have password)
        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please login with Google or Apple"
            )

        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()

        # Create tokens
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "name": user.name,
                "tier": user.subscription.tier.value if user.subscription else "free",
            }
        )

        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}
        )

        return user, access_token, refresh_token

    def _create_free_subscription(self, user_id: int) -> Subscription:
        """Create a free subscription for new user"""
        subscription = Subscription(
            user_id=user_id,
            tier=SubscriptionTier.FREE,
            status=SubscriptionStatus.ACTIVE,
        )
        self.db.add(subscription)
        self.db.commit()
        return subscription

    def _create_user_stats(self, user_id: int) -> UserStats:
        """Create initial user stats for gamification"""
        stats = UserStats(
            user_id=user_id,
            karma_points=0,
            badges=[],
            daily_quests={},
        )
        self.db.add(stats)
        self.db.commit()
        return stats

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
