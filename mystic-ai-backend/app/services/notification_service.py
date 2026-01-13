"""
Notification Service - Firebase Cloud Messaging integration
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, time, timedelta
import logging
import json

try:
    import firebase_admin
    from firebase_admin import credentials, messaging
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Warning: firebase-admin not installed. Push notifications will be disabled.")

from app.models.user import User
from app.models.notification import (
    NotificationToken,
    NotificationHistory,
    NotificationPreferences,
    DevicePlatform,
    NotificationType
)
from app.schemas.notification import (
    NotificationTokenCreate,
    NotificationSend,
    NotificationPreferencesUpdate
)
from app.config import settings
from app.services.moon_phase import MoonPhaseService

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for managing push notifications via Firebase Cloud Messaging

    Features:
    - Device token registration and management
    - Push notification sending (FCM)
    - Notification preferences management
    - Quiet hours support
    - Notification history tracking
    - Automated notifications (daily affirmation, reminders, etc.)
    """

    def __init__(self, db: Session):
        """
        Initialize notification service

        Args:
            db: Database session
        """
        self.db = db
        self.firebase_initialized = False
        self.moon_service = MoonPhaseService()

        # Initialize Firebase if credentials are available
        if FIREBASE_AVAILABLE and settings.FIREBASE_PROJECT_ID:
            try:
                # Check if Firebase is already initialized
                if not firebase_admin._apps:
                    cred_dict = {
                        "type": "service_account",
                        "project_id": settings.FIREBASE_PROJECT_ID,
                        "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
                        "private_key": settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
                        "client_email": f"firebase-adminsdk@{settings.FIREBASE_PROJECT_ID}.iam.gserviceaccount.com",
                    }
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)

                self.firebase_initialized = True
                logger.info("Firebase Cloud Messaging initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Firebase: {e}")
                self.firebase_initialized = False
        else:
            logger.warning("Firebase credentials not configured. Push notifications disabled.")

    def is_available(self) -> bool:
        """Check if push notifications are available"""
        return FIREBASE_AVAILABLE and self.firebase_initialized

    async def register_device(
        self,
        user: User,
        token_data: NotificationTokenCreate
    ) -> NotificationToken:
        """
        Register a device token for push notifications

        Args:
            user: User object
            token_data: Token registration data

        Returns:
            NotificationToken object
        """

        # Check if token already exists
        existing_token = (
            self.db.query(NotificationToken)
            .filter(NotificationToken.token == token_data.token)
            .first()
        )

        if existing_token:
            # Update existing token
            existing_token.user_id = user.id
            existing_token.platform = token_data.platform
            existing_token.device_id = token_data.device_id
            existing_token.device_name = token_data.device_name
            existing_token.is_active = True
            existing_token.last_used = datetime.utcnow()

            self.db.commit()
            self.db.refresh(existing_token)

            logger.info(f"Updated device token for user {user.id}")
            return existing_token

        # Create new token
        token = NotificationToken(
            user_id=user.id,
            token=token_data.token,
            platform=token_data.platform,
            device_id=token_data.device_id,
            device_name=token_data.device_name
        )

        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)

        logger.info(f"Registered new device token for user {user.id}")

        # Create default notification preferences if not exists
        await self._ensure_preferences(user)

        return token

    async def _ensure_preferences(self, user: User) -> NotificationPreferences:
        """Ensure user has notification preferences"""

        prefs = (
            self.db.query(NotificationPreferences)
            .filter(NotificationPreferences.user_id == user.id)
            .first()
        )

        if not prefs:
            prefs = NotificationPreferences(user_id=user.id)
            self.db.add(prefs)
            self.db.commit()
            self.db.refresh(prefs)
            logger.info(f"Created default notification preferences for user {user.id}")

        return prefs

    async def unregister_device(self, user: User, token: str) -> bool:
        """
        Unregister a device token

        Args:
            user: User object
            token: FCM token to remove

        Returns:
            Success status
        """

        result = (
            self.db.query(NotificationToken)
            .filter(
                NotificationToken.user_id == user.id,
                NotificationToken.token == token
            )
            .delete()
        )

        self.db.commit()

        if result > 0:
            logger.info(f"Unregistered device token for user {user.id}")
            return True

        return False

    async def get_user_tokens(self, user: User) -> List[NotificationToken]:
        """Get all active tokens for a user"""

        tokens = (
            self.db.query(NotificationToken)
            .filter(
                NotificationToken.user_id == user.id,
                NotificationToken.is_active == True
            )
            .all()
        )

        return tokens

    async def send_notification(
        self,
        user: User,
        notification_data: NotificationSend
    ) -> bool:
        """
        Send push notification to user's devices

        Args:
            user: User object
            notification_data: Notification content

        Returns:
            Success status
        """

        # Check if notifications are available
        if not self.is_available():
            logger.warning("Firebase not available. Skipping notification send.")
            return False

        # Check user preferences
        prefs = await self._ensure_preferences(user)
        if not self._check_notification_allowed(prefs, notification_data.notification_type):
            logger.info(f"User {user.id} has disabled {notification_data.notification_type} notifications")
            return False

        # Check quiet hours
        if not self._check_quiet_hours(prefs):
            logger.info(f"Notification skipped due to quiet hours for user {user.id}")
            return False

        # Get active tokens
        tokens = await self.get_user_tokens(user)

        if not tokens:
            logger.warning(f"No active tokens for user {user.id}")
            return False

        # Create notification history record
        history = NotificationHistory(
            user_id=user.id,
            notification_type=notification_data.notification_type,
            title=notification_data.title,
            body=notification_data.body,
            data=json.dumps(notification_data.data) if notification_data.data else None
        )

        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)

        # Send via FCM
        try:
            # Build FCM message
            message = messaging.MulticastMessage(
                tokens=[t.token for t in tokens],
                notification=messaging.Notification(
                    title=notification_data.title,
                    body=notification_data.body
                ),
                data=notification_data.data if notification_data.data else {},
                android=messaging.AndroidConfig(
                    priority="high",
                    notification=messaging.AndroidNotification(
                        sound="default",
                        channel_id="mystic_ai_default"
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound="default",
                            badge=1
                        )
                    )
                )
            )

            # Send message
            response = messaging.send_multicast(message)

            # Update history
            history.sent = True
            history.sent_at = datetime.utcnow()

            if response.success_count > 0:
                history.delivered = True
                history.delivered_at = datetime.utcnow()

            if response.failure_count > 0:
                # Log failures
                for idx, resp in enumerate(response.responses):
                    if not resp.success:
                        logger.error(f"Failed to send to token {tokens[idx].token}: {resp.exception}")

            self.db.commit()

            logger.info(f"Sent notification to user {user.id}: {response.success_count} succeeded, {response.failure_count} failed")

            return response.success_count > 0

        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            history.error_message = str(e)[:500]
            self.db.commit()
            return False

    def _check_notification_allowed(
        self,
        prefs: NotificationPreferences,
        notification_type: NotificationType
    ) -> bool:
        """Check if notification type is allowed by user preferences"""

        type_mapping = {
            NotificationType.DAILY_AFFIRMATION: prefs.daily_affirmation,
            NotificationType.READING_REMINDER: prefs.reading_reminder,
            NotificationType.JOURNAL_REMINDER: prefs.journal_reminder,
            NotificationType.MOON_PHASE: prefs.moon_phase,
            NotificationType.STREAK_MILESTONE: prefs.streak_milestone,
            NotificationType.NEW_FEATURE: prefs.new_feature,
            NotificationType.SUBSCRIPTION_EXPIRY: prefs.subscription_expiry,
            NotificationType.CUSTOM: True  # Always allow custom notifications
        }

        return type_mapping.get(notification_type, True)

    def _check_quiet_hours(self, prefs: NotificationPreferences) -> bool:
        """Check if current time is within quiet hours"""

        if not prefs.quiet_hours_enabled:
            return True

        if not prefs.quiet_hours_start or not prefs.quiet_hours_end:
            return True

        now = datetime.utcnow().time()

        # Parse quiet hours
        start_time = time.fromisoformat(prefs.quiet_hours_start)
        end_time = time.fromisoformat(prefs.quiet_hours_end)

        # Handle overnight quiet hours (e.g., 22:00 - 08:00)
        if start_time > end_time:
            return not (now >= start_time or now < end_time)
        else:
            return not (start_time <= now < end_time)

    async def update_preferences(
        self,
        user: User,
        preferences_update: NotificationPreferencesUpdate
    ) -> NotificationPreferences:
        """Update user notification preferences"""

        prefs = await self._ensure_preferences(user)

        # Update fields
        update_data = preferences_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(prefs, field, value)

        prefs.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(prefs)

        logger.info(f"Updated notification preferences for user {user.id}")

        return prefs

    async def get_preferences(self, user: User) -> NotificationPreferences:
        """Get user notification preferences"""
        return await self._ensure_preferences(user)

    async def send_daily_affirmation(self, user: User, affirmation: str) -> bool:
        """Send daily affirmation notification"""

        notification = NotificationSend(
            notification_type=NotificationType.DAILY_AFFIRMATION,
            title="Your Daily Affirmation ✨",
            body=affirmation,
            data={"type": "daily_affirmation"}
        )

        return await self.send_notification(user, notification)

    async def send_moon_phase_notification(self, user: User) -> bool:
        """Send moon phase notification"""

        moon_data = self.moon_service.get_current_phase()

        notification = NotificationSend(
            notification_type=NotificationType.MOON_PHASE,
            title=f"{moon_data['emoji']} {moon_data['phase_name']} Today",
            body=f"{moon_data['meaning']['energy']}. {moon_data['meaning']['guidance'][:100]}...",
            data={
                "type": "moon_phase",
                "phase": moon_data['phase_key']
            }
        )

        return await self.send_notification(user, notification)

    async def send_streak_milestone(self, user: User, streak_days: int) -> bool:
        """Send streak milestone notification"""

        notification = NotificationSend(
            notification_type=NotificationType.STREAK_MILESTONE,
            title=f"🔥 {streak_days}-Day Streak!",
            body=f"Amazing! You've journaled {streak_days} days in a row. Keep the momentum going!",
            data={
                "type": "streak_milestone",
                "streak": streak_days
            }
        )

        return await self.send_notification(user, notification)

    async def send_journal_reminder(self, user: User) -> bool:
        """Send journal reminder notification"""

        notification = NotificationSend(
            notification_type=NotificationType.JOURNAL_REMINDER,
            title="Time to Reflect 📝",
            body="Take a moment to journal about your day. How are you feeling?",
            data={"type": "journal_reminder"}
        )

        return await self.send_notification(user, notification)

    async def get_notification_history(
        self,
        user: User,
        limit: int = 50,
        offset: int = 0
    ) -> List[NotificationHistory]:
        """Get user's notification history"""

        history = (
            self.db.query(NotificationHistory)
            .filter(NotificationHistory.user_id == user.id)
            .order_by(NotificationHistory.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return history

    async def mark_notification_opened(self, history_id: int, user: User) -> bool:
        """Mark a notification as opened"""

        history = (
            self.db.query(NotificationHistory)
            .filter(
                NotificationHistory.id == history_id,
                NotificationHistory.user_id == user.id
            )
            .first()
        )

        if not history:
            return False

        history.opened = True
        history.opened_at = datetime.utcnow()

        self.db.commit()

        return True
