"""
Webhook API endpoints - Handle payment provider webhooks
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Header, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.db.session import get_db
from app.services.webhook_service import WebhookService
from app.schemas.webhook import WebhookResponse, WebhookEventResponse
from app.utils.webhook_verification import verify_revenuecat_webhook
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/revenuecat", response_model=WebhookResponse, status_code=status.HTTP_200_OK)
async def handle_revenuecat_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_revenuecat_signature: Optional[str] = Header(None, alias="X-RevenueCat-Signature")
):
    """
    Handle RevenueCat webhook events

    **No authentication required** - This endpoint is called by RevenueCat servers

    **Security:**
    - Verifies webhook signature using REVENUECAT_WEBHOOK_SECRET
    - Logs all events for audit trail
    - Idempotent processing (duplicate events are handled safely)

    **Supported Events:**
    - INITIAL_PURCHASE: First subscription purchase
    - RENEWAL: Subscription renewed
    - CANCELLATION: User cancelled subscription
    - UNCANCELLATION: User resumed subscription
    - EXPIRATION: Subscription expired
    - BILLING_ISSUE: Payment failed
    - PRODUCT_CHANGE: Plan upgraded/downgraded

    **Response:**
    Returns 200 OK even if processing fails (to prevent retries for invalid data)

    **Testing:**
    Use RevenueCat dashboard to send test webhooks:
    https://app.revenuecat.com/webhooks
    """
    # Get raw body for signature verification
    body = await request.body()

    # Get client info
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    # Verify signature
    is_valid = verify_revenuecat_webhook(
        payload=body,
        signature=x_revenuecat_signature
    )

    if not is_valid:
        logger.warning(f"Invalid webhook signature from {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature"
        )

    # Parse JSON payload
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse webhook JSON: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload"
        )

    # Process webhook
    webhook_service = WebhookService(db)

    try:
        webhook_event = webhook_service.process_revenuecat_webhook(
            payload=payload,
            ip_address=client_ip,
            user_agent=user_agent
        )

        return WebhookResponse(
            success=True,
            message="Webhook processed successfully",
            event_id=webhook_event.event_id
        )

    except ValueError as e:
        # Invalid payload format
        logger.error(f"Invalid webhook payload: {str(e)}")
        # Return 200 to prevent retries
        return WebhookResponse(
            success=False,
            message=f"Invalid payload: {str(e)}"
        )

    except Exception as e:
        # Processing error
        logger.error(f"Webhook processing error: {str(e)}")
        # Return 200 to prevent retries for permanent errors
        return WebhookResponse(
            success=False,
            message=f"Processing error: {str(e)}"
        )


@router.get("/events", response_model=list[WebhookEventResponse])
def list_webhook_events(
    source: Optional[str] = None,
    processed: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List webhook events (admin only)

    **Requires:** Authentication (admin user)

    **Query Parameters:**
    - `source`: Filter by source (revenuecat, stripe, etc.)
    - `processed`: Filter by processed status (true/false)
    - `limit`: Number of events to return (max 100)
    - `offset`: Pagination offset

    **Returns:** List of webhook events

    **Use Case:** Debugging and monitoring webhook processing
    """
    # TODO: Add admin check
    # For now, just require authentication

    if limit > 100:
        limit = 100

    webhook_service = WebhookService(db)
    events = webhook_service.get_webhook_events(
        source=source,
        processed=processed,
        limit=limit,
        offset=offset
    )

    return [WebhookEventResponse.from_orm(event) for event in events]


@router.post("/events/{event_id}/retry", response_model=WebhookEventResponse)
def retry_webhook_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retry a failed webhook event (admin only)

    **Requires:** Authentication (admin user)

    **Path Parameters:**
    - `event_id`: Webhook event ID to retry

    **Returns:** Updated webhook event

    **Use Case:** Manually retry webhooks that failed due to temporary errors
    """
    # TODO: Add admin check

    webhook_service = WebhookService(db)

    try:
        event = webhook_service.retry_failed_webhook(event_id)
        return WebhookEventResponse.from_orm(event)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retry failed: {str(e)}"
        )


# Placeholder for Stripe webhooks (if needed in future)
@router.post("/stripe", response_model=WebhookResponse)
async def handle_stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
    stripe_signature: Optional[str] = Header(None, alias="Stripe-Signature")
):
    """
    Handle Stripe webhook events

    **Status:** Not yet implemented

    Placeholder for future Stripe integration if needed.
    """
    return WebhookResponse(
        success=False,
        message="Stripe webhooks not yet implemented"
    )
