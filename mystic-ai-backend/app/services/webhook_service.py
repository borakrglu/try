"""
Webhook Service - Handles incoming webhooks from payment providers
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timezone

from app.models.user import User
from app.models.subscription import Subscription, SubscriptionTier
from app.models.webhook_event import WebhookEvent
from app.schemas.webhook import RevenueCatEvent, RevenueCatEventType

logger = logging.getLogger(__name__)


class WebhookService:
    """Service for processing webhook events"""

    def __init__(self, db: Session):
        self.db = db

    def process_revenuecat_webhook(
        self,
        payload: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> WebhookEvent:
        """
        Process RevenueCat webhook event

        Args:
            payload: Raw webhook payload
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            WebhookEvent record
        """
        # Parse event
        try:
            event = RevenueCatEvent(**payload)
        except Exception as e:
            logger.error(f"Failed to parse RevenueCat webhook: {str(e)}")
            raise ValueError(f"Invalid webhook payload: {str(e)}")

        # Create webhook event record
        webhook_event = WebhookEvent(
            source="revenuecat",
            event_type=event.event.value,
            event_id=f"{event.app_user_id}_{event.event.value}_{event.purchased_at_ms or int(datetime.now().timestamp() * 1000)}",
            payload=payload,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        self.db.add(webhook_event)
        self.db.commit()
        self.db.refresh(webhook_event)

        logger.info(f"Webhook event created: {webhook_event.id} ({event.event.value})")

        # Process the event
        try:
            self._handle_revenuecat_event(event, webhook_event)
            webhook_event.mark_as_processed()
            self.db.commit()
            logger.info(f"Webhook {webhook_event.id} processed successfully")
        except Exception as e:
            error_msg = f"Failed to process webhook: {str(e)}"
            logger.error(error_msg)
            webhook_event.mark_as_failed(error_msg)
            self.db.commit()
            raise

        return webhook_event

    def _handle_revenuecat_event(
        self,
        event: RevenueCatEvent,
        webhook_event: WebhookEvent
    ):
        """
        Handle specific RevenueCat event types

        Args:
            event: Parsed RevenueCat event
            webhook_event: Database webhook event record
        """
        # Find user by app_user_id (should match our user.id)
        user = self._find_user_by_app_user_id(event.app_user_id)

        if not user:
            logger.warning(f"User not found for app_user_id: {event.app_user_id}")
            webhook_event.user_id = None
            return

        webhook_event.user_id = user.id

        # Route to appropriate handler
        if event.event == RevenueCatEventType.INITIAL_PURCHASE:
            self._handle_initial_purchase(user, event)
        elif event.event == RevenueCatEventType.RENEWAL:
            self._handle_renewal(user, event)
        elif event.event == RevenueCatEventType.CANCELLATION:
            self._handle_cancellation(user, event)
        elif event.event == RevenueCatEventType.UNCANCELLATION:
            self._handle_uncancellation(user, event)
        elif event.event == RevenueCatEventType.EXPIRATION:
            self._handle_expiration(user, event)
        elif event.event == RevenueCatEventType.BILLING_ISSUE:
            self._handle_billing_issue(user, event)
        elif event.event == RevenueCatEventType.PRODUCT_CHANGE:
            self._handle_product_change(user, event)
        else:
            logger.info(f"Event type {event.event.value} - no specific handler")

    def _find_user_by_app_user_id(self, app_user_id: str) -> Optional[User]:
        """Find user by RevenueCat app_user_id"""
        try:
            user_id = int(app_user_id)
            return self.db.query(User).filter(User.id == user_id).first()
        except ValueError:
            logger.warning(f"Invalid app_user_id format: {app_user_id}")
            return None

    def _handle_initial_purchase(self, user: User, event: RevenueCatEvent):
        """Handle initial purchase event"""
        logger.info(f"User {user.id} - Initial purchase: {event.product_id}")

        subscription = user.subscription

        # Determine tier from product_id
        tier = self._get_tier_from_product_id(event.product_id)

        # Update subscription
        subscription.tier = tier
        subscription.is_active = True
        subscription.is_trial = (event.period_type == "TRIAL")
        subscription.cancelled_at = None

        # Set expiration date
        if event.expiration_at_ms:
            subscription.current_period_end = datetime.fromtimestamp(
                event.expiration_at_ms / 1000, tz=timezone.utc
            )

        # Store RevenueCat info
        subscription.revenuecat_id = event.app_user_id
        subscription.product_id = event.product_id
        subscription.store = event.store

        self.db.commit()

        logger.info(f"User {user.id} upgraded to {tier.value}")

    def _handle_renewal(self, user: User, event: RevenueCatEvent):
        """Handle subscription renewal"""
        logger.info(f"User {user.id} - Renewal: {event.product_id}")

        subscription = user.subscription

        # Update subscription
        subscription.is_active = True
        subscription.is_trial = False  # Trial ended

        # Update expiration
        if event.expiration_at_ms:
            subscription.current_period_end = datetime.fromtimestamp(
                event.expiration_at_ms / 1000, tz=timezone.utc
            )

        # Reset monthly usage counters on renewal
        subscription.readings_this_month = 0
        subscription.chat_messages_today = 0

        self.db.commit()

        logger.info(f"User {user.id} subscription renewed until {subscription.current_period_end}")

    def _handle_cancellation(self, user: User, event: RevenueCatEvent):
        """Handle subscription cancellation"""
        logger.info(f"User {user.id} - Cancellation")

        subscription = user.subscription

        # Mark as cancelled but keep active until period end
        subscription.cancelled_at = datetime.utcnow()
        # is_active stays True until expiration

        self.db.commit()

        logger.info(f"User {user.id} subscription cancelled (active until {subscription.current_period_end})")

    def _handle_uncancellation(self, user: User, event: RevenueCatEvent):
        """Handle subscription uncancellation (re-enabled before expiry)"""
        logger.info(f"User {user.id} - Uncancellation")

        subscription = user.subscription

        # Remove cancellation
        subscription.cancelled_at = None
        subscription.is_active = True

        self.db.commit()

        logger.info(f"User {user.id} subscription reactivated")

    def _handle_expiration(self, user: User, event: RevenueCatEvent):
        """Handle subscription expiration"""
        logger.info(f"User {user.id} - Expiration")

        subscription = user.subscription

        # Downgrade to free tier
        subscription.tier = SubscriptionTier.FREE
        subscription.is_active = False
        subscription.is_trial = False

        # Reset usage counters
        subscription.readings_this_month = 0
        subscription.chat_messages_today = 0

        self.db.commit()

        logger.info(f"User {user.id} subscription expired, downgraded to FREE")

    def _handle_billing_issue(self, user: User, event: RevenueCatEvent):
        """Handle billing issues (payment failure)"""
        logger.warning(f"User {user.id} - Billing issue")

        subscription = user.subscription

        # Mark billing issue but keep subscription active temporarily
        # RevenueCat will send EXPIRATION if grace period passes
        # For now, just log it

        logger.info(f"User {user.id} has billing issues")

    def _handle_product_change(self, user: User, event: RevenueCatEvent):
        """Handle product change (upgrade/downgrade)"""
        logger.info(f"User {user.id} - Product change to {event.product_id}")

        subscription = user.subscription

        # Update to new tier
        tier = self._get_tier_from_product_id(event.product_id)
        subscription.tier = tier
        subscription.product_id = event.product_id

        # Update expiration
        if event.expiration_at_ms:
            subscription.current_period_end = datetime.fromtimestamp(
                event.expiration_at_ms / 1000, tz=timezone.utc
            )

        self.db.commit()

        logger.info(f"User {user.id} subscription changed to {tier.value}")

    def _get_tier_from_product_id(self, product_id: Optional[str]) -> SubscriptionTier:
        """
        Determine subscription tier from product ID

        Product ID format: mystic_weekly, mystic_monthly, etc.
        """
        if not product_id:
            return SubscriptionTier.FREE

        product_id_lower = product_id.lower()

        if "weekly" in product_id_lower or "week" in product_id_lower:
            return SubscriptionTier.PREMIUM_WEEKLY
        elif "monthly" in product_id_lower or "month" in product_id_lower:
            return SubscriptionTier.PREMIUM_MONTHLY
        else:
            logger.warning(f"Unknown product_id: {product_id}, defaulting to MONTHLY")
            return SubscriptionTier.PREMIUM_MONTHLY

    def get_webhook_events(
        self,
        source: Optional[str] = None,
        processed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[WebhookEvent]:
        """
        Get webhook events with filters

        Args:
            source: Filter by source (revenuecat, stripe, etc.)
            processed: Filter by processed status
            limit: Number of records to return
            offset: Pagination offset

        Returns:
            List of webhook events
        """
        query = self.db.query(WebhookEvent)

        if source:
            query = query.filter(WebhookEvent.source == source)

        if processed is not None:
            query = query.filter(WebhookEvent.processed == processed)

        events = query.order_by(WebhookEvent.received_at.desc()).limit(limit).offset(offset).all()

        return events

    def retry_failed_webhook(self, webhook_id: int) -> WebhookEvent:
        """
        Retry processing a failed webhook

        Args:
            webhook_id: Webhook event ID

        Returns:
            Updated webhook event
        """
        webhook_event = self.db.query(WebhookEvent).filter(
            WebhookEvent.id == webhook_id
        ).first()

        if not webhook_event:
            raise ValueError(f"Webhook event {webhook_id} not found")

        if webhook_event.processed:
            raise ValueError(f"Webhook {webhook_id} already processed")

        logger.info(f"Retrying webhook {webhook_id}")

        # Re-parse and process
        try:
            event = RevenueCatEvent(**webhook_event.payload)
            self._handle_revenuecat_event(event, webhook_event)
            webhook_event.mark_as_processed()
            self.db.commit()
            logger.info(f"Webhook {webhook_id} retry successful")
        except Exception as e:
            error_msg = f"Retry failed: {str(e)}"
            logger.error(error_msg)
            webhook_event.mark_as_failed(error_msg)
            self.db.commit()
            raise

        return webhook_event
