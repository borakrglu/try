"""
Pydantic schemas package
"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserCreateOAuth,
    UserUpdate,
    UserResponse,
    UserWithSubscription,
)
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    OAuthLoginRequest,
    TokenPayload,
    RefreshTokenRequest,
    TokenResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
    ChangePasswordRequest,
)
from app.schemas.reading import (
    CoffeeReadingCreate,
    TarotReadingCreate,
    TarotCard,
    PalmReadingCreate,
    SymbolDetected,
    ReadingImageResponse,
    ReadingResponse,
    ReadingFeedback,
    ReadingListResponse,
)
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatHistoryResponse,
    ChatStreamChunk,
)
from app.schemas.journal import (
    JournalEntryCreate,
    JournalEntryUpdate,
    JournalEntryResponse,
    ChakraInsights,
    MoodInsights,
    JournalInsightsResponse,
    MoodCalendarDay,
    MoodCalendarResponse,
)
from app.schemas.subscription import (
    ReceiptVerifyRequest,
    SubscriptionResponse,
    UsageStatusResponse,
    SubscriptionCancelRequest,
    RevenueCatWebhook,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserCreateOAuth",
    "UserUpdate",
    "UserResponse",
    "UserWithSubscription",
    # Auth
    "LoginRequest",
    "LoginResponse",
    "OAuthLoginRequest",
    "TokenPayload",
    "RefreshTokenRequest",
    "TokenResponse",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "ChangePasswordRequest",
    # Reading
    "CoffeeReadingCreate",
    "TarotReadingCreate",
    "TarotCard",
    "PalmReadingCreate",
    "SymbolDetected",
    "ReadingImageResponse",
    "ReadingResponse",
    "ReadingFeedback",
    "ReadingListResponse",
    # Chat
    "ChatMessageCreate",
    "ChatMessageResponse",
    "ChatHistoryResponse",
    "ChatStreamChunk",
    # Journal
    "JournalEntryCreate",
    "JournalEntryUpdate",
    "JournalEntryResponse",
    "ChakraInsights",
    "MoodInsights",
    "JournalInsightsResponse",
    "MoodCalendarDay",
    "MoodCalendarResponse",
    # Subscription
    "ReceiptVerifyRequest",
    "SubscriptionResponse",
    "UsageStatusResponse",
    "SubscriptionCancelRequest",
    "RevenueCatWebhook",
]
