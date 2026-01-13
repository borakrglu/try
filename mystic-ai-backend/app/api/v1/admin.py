"""
Admin API endpoints - Platform administration and monitoring
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, EmailStr

from app.db.session import get_db
from app.api.deps import get_admin_user
from app.models.user import User
from app.models.subscription import SubscriptionTier
from app.services.admin_service import AdminService

router = APIRouter()


# Schemas for admin operations
class UserBanRequest(BaseModel):
    """Schema for banning a user"""
    reason: str


class UserSearchResponse(BaseModel):
    """Schema for user search results"""
    id: int
    email: str
    name: str
    zodiac_sign: Optional[str]
    is_admin: bool
    is_banned: bool
    ban_reason: Optional[str]
    created_at: str
    last_login: Optional[str]

    class Config:
        from_attributes = True


@router.get("/users")
async def list_users(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None, description="Search by name or email"),
    tier: Optional[SubscriptionTier] = Query(None, description="Filter by subscription tier"),
    banned_only: bool = Query(False, description="Show only banned users"),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all users with filtering and pagination

    **Admin only** 🔐

    **Query Parameters:**
    - **limit**: Number of users (1-100, default: 50)
    - **offset**: Pagination offset (default: 0)
    - **search**: Search by name or email
    - **tier**: Filter by subscription (FREE/WEEKLY/MONTHLY/ANNUAL)
    - **banned_only**: Show only banned users

    **Returns:**
    List of users with pagination info

    **Example:**
    `/api/v1/admin/users?search=luna&tier=MONTHLY&limit=20`
    """

    admin_service = AdminService(db)

    try:
        result = await admin_service.get_users(
            limit=limit,
            offset=offset,
            search=search,
            tier=tier,
            banned_only=banned_only
        )

        return {
            "users": [
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "zodiac_sign": user.zodiac_sign,
                    "is_admin": user.is_admin,
                    "is_banned": user.is_banned,
                    "ban_reason": user.ban_reason,
                    "created_at": user.created_at.isoformat(),
                    "last_login": user.last_login.isoformat() if user.last_login else None
                }
                for user in result["users"]
            ],
            "total": result["total"],
            "limit": result["limit"],
            "offset": result["offset"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )


@router.get("/users/{user_id}")
async def get_user_details(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific user

    **Admin only** 🔐

    **Path Parameters:**
    - **user_id**: User ID

    **Returns:**
    Complete user information including subscription, stats, and activity

    **Example Response:**
    ```json
    {
      "id": 123,
      "email": "luna@example.com",
      "name": "Luna",
      "is_admin": false,
      "is_banned": false,
      "subscription": {
        "tier": "MONTHLY",
        "is_active": true,
        "readings_this_month": 15
      },
      "stats": {
        "karma_points": 450,
        "total_readings": 42,
        "journal_entries": 28
      }
    }
    ```
    """

    admin_service = AdminService(db)

    user = await admin_service.get_user_details(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "zodiac_sign": user.zodiac_sign,
        "language": user.language.value if user.language else None,
        "is_admin": user.is_admin,
        "is_banned": user.is_banned,
        "ban_reason": user.ban_reason,
        "created_at": user.created_at.isoformat(),
        "last_login": user.last_login.isoformat() if user.last_login else None,
        "subscription": {
            "tier": user.subscription.tier.value if user.subscription else "FREE",
            "is_active": user.subscription.is_active if user.subscription else False,
            "readings_this_month": user.subscription.readings_this_month if user.subscription else 0,
            "chat_messages_today": user.subscription.chat_messages_today if user.subscription else 0
        } if user.subscription else None,
        "stats": {
            "karma_points": user.stats.karma_points if user.stats else 0,
            "total_readings": user.stats.total_readings if user.stats else 0,
            "journal_entries": user.stats.journal_entries if user.stats else 0,
            "current_journal_streak": user.stats.current_journal_streak if user.stats else 0
        } if user.stats else None
    }


@router.post("/users/{user_id}/ban")
async def ban_user(
    user_id: int,
    ban_request: UserBanRequest,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Ban a user from the platform

    **Admin only** 🔐

    **Path Parameters:**
    - **user_id**: User ID to ban

    **Request Body:**
    - **reason**: Ban reason (required)

    **Returns:**
    Confirmation message

    **Example:**
    ```json
    {
      "reason": "Spam and abusive content"
    }
    ```

    **Note:** Cannot ban other admin users.
    """

    admin_service = AdminService(db)

    user = await admin_service.ban_user(user_id, ban_request.reason, admin)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or cannot be banned (may be admin)"
        )

    return {
        "message": f"User {user.email} has been banned",
        "user_id": user.id,
        "ban_reason": user.ban_reason
    }


@router.post("/users/{user_id}/unban")
async def unban_user(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Unban a user

    **Admin only** 🔐

    **Path Parameters:**
    - **user_id**: User ID to unban

    **Returns:**
    Confirmation message
    """

    admin_service = AdminService(db)

    user = await admin_service.unban_user(user_id, admin)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "message": f"User {user.email} has been unbanned",
        "user_id": user.id
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Permanently delete a user and all their data

    **Admin only** 🔐 **DESTRUCTIVE**

    **Warning:** This action cannot be undone!
    All user data will be permanently deleted:
    - Readings, chat messages, journal entries
    - Subscription and payment history
    - Notification tokens and preferences
    - Stats and badges

    **Path Parameters:**
    - **user_id**: User ID to delete

    **Returns:**
    Confirmation message

    **Note:** Cannot delete other admin users.
    """

    admin_service = AdminService(db)

    success = await admin_service.delete_user(user_id, admin)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or cannot be deleted (may be admin)"
        )

    return {
        "message": f"User {user_id} has been permanently deleted"
    }


@router.post("/users/{user_id}/promote")
async def promote_to_admin(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Promote a user to admin

    **Admin only** 🔐

    **Path Parameters:**
    - **user_id**: User ID to promote

    **Returns:**
    Confirmation message
    """

    admin_service = AdminService(db)

    user = await admin_service.promote_to_admin(user_id, admin)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "message": f"User {user.email} has been promoted to admin",
        "user_id": user.id
    }


@router.get("/stats")
async def get_system_stats(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive system statistics

    **Admin only** 🔐

    **Returns:**
    Complete platform metrics including:
    - User statistics (total, new, premium)
    - Reading statistics (total, by type)
    - Chat and journal activity
    - Webhook status
    - Top users by karma

    **Example Response:**
    ```json
    {
      "users": {
        "total": 1523,
        "banned": 12,
        "new_7d": 87,
        "new_30d": 342,
        "premium": 234,
        "tier_breakdown": {
          "FREE": 1289,
          "WEEKLY": 45,
          "MONTHLY": 156,
          "ANNUAL": 33
        }
      },
      "readings": {
        "total": 6789,
        "last_7_days": 523,
        "by_type": {
          "COFFEE": 2345,
          "TAROT": 3123,
          "PALM": 1321
        }
      },
      "top_users": [...]
    }
    ```
    """

    admin_service = AdminService(db)

    try:
        stats = await admin_service.get_system_stats()
        return stats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve system stats: {str(e)}"
        )


@router.get("/stats/revenue")
async def get_revenue_stats(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get revenue statistics

    **Admin only** 🔐

    **Returns:**
    Revenue metrics including:
    - Active subscriptions by tier
    - MRR (Monthly Recurring Revenue)
    - ARR (Annual Recurring Revenue)
    - Estimated monthly revenue

    **Example Response:**
    ```json
    {
      "active_subscriptions": {
        "weekly": 45,
        "monthly": 156,
        "annual": 33,
        "total": 234
      },
      "mrr": {
        "weekly": 898.20,
        "monthly": 2338.44,
        "annual": 274.89,
        "total": 3511.53
      },
      "arr": 42138.36,
      "estimated_monthly_revenue": 3511.53
    }
    ```

    **Note:** Revenue is estimated based on subscription tiers:
    - Weekly: $4.99/week (~$19.96/month)
    - Monthly: $14.99/month
    - Annual: $99.99/year (~$8.33/month)
    """

    admin_service = AdminService(db)

    try:
        revenue = await admin_service.get_revenue_stats()
        return revenue

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve revenue stats: {str(e)}"
        )


@router.get("/stats/growth")
async def get_growth_metrics(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get growth and engagement metrics

    **Admin only** 🔐

    **Returns:**
    Growth metrics including:
    - DAU/WAU/MAU (Daily/Weekly/Monthly Active Users)
    - Engagement metrics (avg readings, journal entries)
    - Retention rate (7-day)
    - Conversion rate (free → premium)

    **Example Response:**
    ```json
    {
      "active_users": {
        "daily": 234,
        "weekly": 567,
        "monthly": 1123
      },
      "engagement": {
        "avg_readings_per_user": 4.5,
        "avg_journal_entries_per_user": 3.2
      },
      "retention_rate_7d": 37.2,
      "conversion_rate": 15.4
    }
    ```
    """

    admin_service = AdminService(db)

    try:
        growth = await admin_service.get_growth_metrics()
        return growth

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve growth metrics: {str(e)}"
        )


@router.get("/moderation/flagged")
async def get_flagged_content(
    limit: int = Query(50, ge=1, le=100),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get flagged or potentially problematic content

    **Admin only** 🔐

    **Query Parameters:**
    - **limit**: Number of items to return (1-100, default: 50)

    **Returns:**
    List of flagged content requiring review

    **Example Response:**
    ```json
    [
      {
        "type": "journal",
        "id": 456,
        "user_id": 123,
        "concern": "Low energy + negative emotion",
        "sentiment": {
          "primary_emotion": "sadness",
          "energy_level": 2
        },
        "created_at": "2026-01-13T10:00:00Z"
      }
    ]
    ```

    **Note:** This is a placeholder implementation.
    In production, would integrate with:
    - Content moderation APIs (OpenAI Moderation, Perspective API)
    - User reporting system
    - Automated sentiment monitoring
    """

    admin_service = AdminService(db)

    try:
        flagged = await admin_service.get_flagged_content(limit=limit)
        return flagged

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve flagged content: {str(e)}"
        )


@router.get("/health")
def get_system_health(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get system health status

    **Admin only** 🔐

    **Returns:**
    Health check for all system components

    **Example Response:**
    ```json
    {
      "status": "healthy",
      "database": "connected",
      "api": "operational",
      "timestamp": "2026-01-13T10:00:00Z"
    }
    ```
    """

    from datetime import datetime

    # Basic health check
    # In production, would check:
    # - Database connection pool
    # - Redis connection
    # - External API status (OpenAI, Firebase, S3)
    # - Queue health (if using Celery)

    try:
        # Test database connection
        db.execute("SELECT 1")

        return {
            "status": "healthy",
            "database": "connected",
            "api": "operational",
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "api": "degraded",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
