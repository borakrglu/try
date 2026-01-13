"""
Webhook Verification Utilities
"""

import hmac
import hashlib
import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)


def verify_revenuecat_webhook(
    payload: bytes,
    signature: Optional[str],
    secret: Optional[str] = None
) -> bool:
    """
    Verify RevenueCat webhook signature

    Args:
        payload: Raw request body (bytes)
        signature: X-RevenueCat-Signature header value
        secret: Webhook secret (from settings if not provided)

    Returns:
        True if signature is valid, False otherwise
    """
    if not signature:
        logger.warning("No signature provided in webhook request")
        return False

    # Use configured secret or provided secret
    webhook_secret = secret or getattr(settings, 'REVENUECAT_WEBHOOK_SECRET', None)

    if not webhook_secret:
        logger.warning("REVENUECAT_WEBHOOK_SECRET not configured, skipping verification")
        # In development, you might want to allow unverified webhooks
        if settings.APP_ENV == "development":
            return True
        return False

    try:
        # Compute expected signature
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        # Compare signatures
        is_valid = hmac.compare_digest(signature, expected_signature)

        if not is_valid:
            logger.warning("Webhook signature verification failed")

        return is_valid

    except Exception as e:
        logger.error(f"Webhook verification error: {str(e)}")
        return False


def verify_stripe_webhook(
    payload: bytes,
    signature: Optional[str],
    secret: Optional[str] = None
) -> bool:
    """
    Verify Stripe webhook signature

    Args:
        payload: Raw request body (bytes)
        signature: Stripe-Signature header value
        secret: Webhook secret (from settings if not provided)

    Returns:
        True if signature is valid, False otherwise
    """
    if not signature:
        logger.warning("No Stripe signature provided")
        return False

    webhook_secret = secret or getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)

    if not webhook_secret:
        logger.warning("STRIPE_WEBHOOK_SECRET not configured")
        if settings.APP_ENV == "development":
            return True
        return False

    try:
        # Stripe uses a more complex verification process
        # This is a simplified version - in production use stripe.Webhook.construct_event()
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY if hasattr(settings, 'STRIPE_SECRET_KEY') else None

        # Stripe signature format: t=timestamp,v1=signature
        # Parse timestamp and signature
        elements = signature.split(',')
        timestamp = None
        signatures = []

        for element in elements:
            if element.startswith('t='):
                timestamp = element[2:]
            elif element.startswith('v1='):
                signatures.append(element[3:])

        if not timestamp or not signatures:
            logger.warning("Invalid Stripe signature format")
            return False

        # Create signed payload
        signed_payload = f"{timestamp}.{payload.decode('utf-8')}"

        # Compute expected signature
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            signed_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Compare with any of the provided signatures
        is_valid = any(
            hmac.compare_digest(expected_signature, sig)
            for sig in signatures
        )

        if not is_valid:
            logger.warning("Stripe webhook signature verification failed")

        return is_valid

    except Exception as e:
        logger.error(f"Stripe webhook verification error: {str(e)}")
        return False
