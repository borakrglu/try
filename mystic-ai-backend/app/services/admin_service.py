"""
Admin Service - User management and system administration
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from app.models.user import User
from app.models.reading import Reading, ReadingType
from app.models.chat import ChatMessage
from app.models.journal import JournalEntry
from app.models.subscription import Subscription, SubscriptionTier
from app.models.user_stats import UserStats
from app.models.webhook_event import WebhookEvent

logger = logging.getLogger(__name__)


class AdminService:
    """
    Service for administrative operations

    Features:
    - User management (list, ban, delete)
    - System statistics and analytics
    - Content moderation
    - Revenue tracking
    - System health monitoring
    """

    def __init__(self, db: Session):
        """
        Initialize admin service

        Args:
            db: Database session
        """
        self.db = db

    async def get_users(
        self,
        limit: int = 50,
        offset: int = 0,
        search: Optional[str] = None,
        tier: Optional[SubscriptionTier] = None,
        banned_only: bool = False
    ) -> Dict[str, Any]:
        """
        Get list of users with filtering

        Args:
            limit: Number of users to return
            offset: Pagination offset
            search: Search by name or email
            tier: Filter by subscription tier
            banned_only: Show only banned users

        Returns:
            Dictionary with users and total count
        """

        query = self.db.query(User)

        # Apply filters
        if search:
            query = query.filter(
                (User.name.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%"))
            )

        if tier:
            query = query.join(Subscription).filter(Subscription.tier == tier)

        if banned_only:
            query = query.filter(User.is_banned == True)

        # Get total count
        total = query.count()

        # Get paginated results
        users = query.order_by(desc(User.created_at)).offset(offset).limit(limit).all()

        return {
            "users": users,
            "total": total,
            "limit": limit,
            "offset": offset
        }

    async def get_user_details(self, user_id: int) -> Optional[User]:
        """Get detailed user information"""
        return self.db.query(User).filter(User.id == user_id).first()

    async def ban_user(
        self,
        user_id: int,
        reason: str,
        admin: User
    ) -> Optional[User]:
        """
        Ban a user

        Args:
            user_id: User ID to ban
            reason: Ban reason
            admin: Admin user performing the action

        Returns:
            Banned user or None
        """

        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        # Don't allow banning admins
        if user.is_admin:
            logger.warning(f"Admin {admin.id} attempted to ban admin {user.id}")
            return None

        user.is_banned = True
        user.ban_reason = reason
        user.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user)

        logger.info(f"User {user_id} banned by admin {admin.id}: {reason}")

        return user

    async def unban_user(self, user_id: int, admin: User) -> Optional[User]:
        """Unban a user"""

        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        user.is_banned = False
        user.ban_reason = None
        user.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user)

        logger.info(f"User {user_id} unbanned by admin {admin.id}")

        return user

    async def delete_user(self, user_id: int, admin: User) -> bool:
        """
        Permanently delete a user and all their data

        Args:
            user_id: User ID to delete
            admin: Admin user performing the action

        Returns:
            Success status
        """

        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return False

        # Don't allow deleting admins
        if user.is_admin:
            logger.warning(f"Admin {admin.id} attempted to delete admin {user.id}")
            return False

        # Cascade delete will handle all relationships
        self.db.delete(user)
        self.db.commit()

        logger.info(f"User {user_id} permanently deleted by admin {admin.id}")

        return True

    async def promote_to_admin(self, user_id: int, admin: User) -> Optional[User]:
        """Promote a user to admin"""

        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        user.is_admin = True
        user.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user)

        logger.info(f"User {user_id} promoted to admin by {admin.id}")

        return user

    async def get_system_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics

        Returns:
            Dictionary with all system metrics
        """

        # User stats
        total_users = self.db.query(func.count(User.id)).scalar()
        banned_users = self.db.query(func.count(User.id)).filter(User.is_banned == True).scalar()

        # New users (last 7 days, 30 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        new_users_7d = self.db.query(func.count(User.id)).filter(User.created_at >= seven_days_ago).scalar()
        new_users_30d = self.db.query(func.count(User.id)).filter(User.created_at >= thirty_days_ago).scalar()

        # Subscription stats
        premium_users = (
            self.db.query(func.count(Subscription.id))
            .filter(Subscription.tier != SubscriptionTier.FREE)
            .scalar()
        )

        tier_breakdown = {}
        for tier in SubscriptionTier:
            count = self.db.query(func.count(Subscription.id)).filter(Subscription.tier == tier).scalar()
            tier_breakdown[tier.value] = count

        # Reading stats
        total_readings = self.db.query(func.count(Reading.id)).scalar()
        readings_7d = self.db.query(func.count(Reading.id)).filter(Reading.created_at >= seven_days_ago).scalar()

        readings_by_type = {}
        for reading_type in ReadingType:
            count = self.db.query(func.count(Reading.id)).filter(Reading.type == reading_type).scalar()
            readings_by_type[reading_type.value] = count

        # Chat stats
        total_chat_messages = self.db.query(func.count(ChatMessage.id)).scalar()
        chat_messages_7d = self.db.query(func.count(ChatMessage.id)).filter(ChatMessage.created_at >= seven_days_ago).scalar()

        # Journal stats
        total_journal_entries = self.db.query(func.count(JournalEntry.id)).scalar()
        journal_entries_7d = self.db.query(func.count(JournalEntry.id)).filter(JournalEntry.created_at >= seven_days_ago).scalar()

        # Webhook stats
        total_webhooks = self.db.query(func.count(WebhookEvent.id)).scalar()
        failed_webhooks = self.db.query(func.count(WebhookEvent.id)).filter(WebhookEvent.processed == False).scalar()

        # Top users by karma
        top_users = (
            self.db.query(User, UserStats)
            .join(UserStats)
            .order_by(desc(UserStats.karma_points))
            .limit(10)
            .all()
        )

        top_users_list = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "karma_points": stats.karma_points,
                "total_readings": stats.total_readings
            }
            for user, stats in top_users
        ]

        return {
            "users": {
                "total": total_users,
                "banned": banned_users,
                "new_7d": new_users_7d,
                "new_30d": new_users_30d,
                "premium": premium_users,
                "tier_breakdown": tier_breakdown
            },
            "readings": {
                "total": total_readings,
                "last_7_days": readings_7d,
                "by_type": readings_by_type
            },
            "chat": {
                "total_messages": total_chat_messages,
                "last_7_days": chat_messages_7d
            },
            "journal": {
                "total_entries": total_journal_entries,
                "last_7_days": journal_entries_7d
            },
            "webhooks": {
                "total": total_webhooks,
                "failed": failed_webhooks
            },
            "top_users": top_users_list
        }

    async def get_revenue_stats(self) -> Dict[str, Any]:
        """
        Get revenue statistics

        Returns:
            Dictionary with revenue metrics
        """

        # Active premium subscriptions
        active_weekly = (
            self.db.query(func.count(Subscription.id))
            .filter(
                Subscription.tier == SubscriptionTier.WEEKLY,
                Subscription.is_active == True
            )
            .scalar()
        )

        active_monthly = (
            self.db.query(func.count(Subscription.id))
            .filter(
                Subscription.tier == SubscriptionTier.MONTHLY,
                Subscription.is_active == True
            )
            .scalar()
        )

        active_annual = (
            self.db.query(func.count(Subscription.id))
            .filter(
                Subscription.tier == SubscriptionTier.ANNUAL,
                Subscription.is_active == True
            )
            .scalar()
        )

        # Estimate MRR (Monthly Recurring Revenue)
        # Weekly: $4.99/week = ~$19.96/month
        # Monthly: $14.99/month
        # Annual: $99.99/year = ~$8.33/month

        mrr_weekly = active_weekly * 19.96
        mrr_monthly = active_monthly * 14.99
        mrr_annual = active_annual * 8.33

        total_mrr = mrr_weekly + mrr_monthly + mrr_annual

        # Estimate ARR (Annual Recurring Revenue)
        arr = total_mrr * 12

        return {
            "active_subscriptions": {
                "weekly": active_weekly,
                "monthly": active_monthly,
                "annual": active_annual,
                "total": active_weekly + active_monthly + active_annual
            },
            "mrr": {
                "weekly": round(mrr_weekly, 2),
                "monthly": round(mrr_monthly, 2),
                "annual": round(mrr_annual, 2),
                "total": round(total_mrr, 2)
            },
            "arr": round(arr, 2),
            "estimated_monthly_revenue": round(total_mrr, 2)
        }

    async def get_growth_metrics(self) -> Dict[str, Any]:
        """
        Get growth and engagement metrics

        Returns:
            Dictionary with growth metrics
        """

        now = datetime.utcnow()

        # Daily active users (last 24 hours)
        dau = (
            self.db.query(func.count(User.id))
            .filter(User.last_login >= now - timedelta(days=1))
            .scalar()
        )

        # Weekly active users (last 7 days)
        wau = (
            self.db.query(func.count(User.id))
            .filter(User.last_login >= now - timedelta(days=7))
            .scalar()
        )

        # Monthly active users (last 30 days)
        mau = (
            self.db.query(func.count(User.id))
            .filter(User.last_login >= now - timedelta(days=30))
            .scalar()
        )

        # Average readings per user
        total_users = self.db.query(func.count(User.id)).scalar()
        total_readings = self.db.query(func.count(Reading.id)).scalar()
        avg_readings_per_user = round(total_readings / total_users, 2) if total_users > 0 else 0

        # Average journal entries per user
        total_journal_entries = self.db.query(func.count(JournalEntry.id)).scalar()
        avg_journal_per_user = round(total_journal_entries / total_users, 2) if total_users > 0 else 0

        # Retention rate (users active in last 7 days / total users)
        retention_rate = round((wau / total_users * 100), 2) if total_users > 0 else 0

        # Conversion rate (premium users / total users)
        premium_users = (
            self.db.query(func.count(Subscription.id))
            .filter(Subscription.tier != SubscriptionTier.FREE)
            .scalar()
        )
        conversion_rate = round((premium_users / total_users * 100), 2) if total_users > 0 else 0

        return {
            "active_users": {
                "daily": dau,
                "weekly": wau,
                "monthly": mau
            },
            "engagement": {
                "avg_readings_per_user": avg_readings_per_user,
                "avg_journal_entries_per_user": avg_journal_per_user
            },
            "retention_rate_7d": retention_rate,
            "conversion_rate": conversion_rate
        }

    async def get_flagged_content(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get flagged or potentially problematic content

        For now, returns placeholder. In production, would check for:
        - Reported chat messages
        - Reported readings
        - Users with negative sentiment patterns
        - Excessive API usage

        Args:
            limit: Number of items to return

        Returns:
            List of flagged content items
        """

        # Placeholder implementation
        # In production, you'd have a separate FlaggedContent model
        # or integrate with content moderation APIs

        flagged_items = []

        # Example: Find users with high negative sentiment in journals
        # This is a simplified example
        recent_journals = (
            self.db.query(JournalEntry)
            .filter(JournalEntry.sentiment_analysis.isnot(None))
            .order_by(desc(JournalEntry.created_at))
            .limit(limit)
            .all()
        )

        for journal in recent_journals:
            if journal.sentiment_analysis:
                sentiment = journal.sentiment_analysis
                # Check for concerning patterns
                if sentiment.get("primary_emotion") in ["anger", "fear", "sadness"]:
                    if sentiment.get("energy_level", 5) < 3:
                        flagged_items.append({
                            "type": "journal",
                            "id": journal.id,
                            "user_id": journal.user_id,
                            "concern": "Low energy + negative emotion",
                            "sentiment": sentiment,
                            "created_at": journal.created_at.isoformat()
                        })

        return flagged_items[:limit]
