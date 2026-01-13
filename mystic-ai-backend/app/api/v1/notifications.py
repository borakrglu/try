"""
Notifications API endpoints - Push notification management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.notification import (
    NotificationTokenCreate,
    NotificationTokenResponse,
    NotificationPreferencesUpdate,
    NotificationPreferencesResponse,
    NotificationSend,
    NotificationHistoryResponse
)
from app.services.notification_service import NotificationService

router = APIRouter()


@router.post("/tokens", response_model=NotificationTokenResponse, status_code=status.HTTP_201_CREATED)
async def register_device_token(
    token_data: NotificationTokenCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Register a device token for push notifications

    **Request Body:**
    - **token**: FCM device token (from Firebase SDK)
    - **platform**: Device platform (ios/android/web)
    - **device_id**: Optional unique device identifier
    - **device_name**: Optional device name (e.g., "iPhone 13 Pro")

    **Returns:**
    Registered notification token with details

    **Example:**
    ```json
    {
      "token": "fK7xJ...long_fcm_token...9pQm",
      "platform": "ios",
      "device_id": "ABC123DEF456",
      "device_name": "Luna's iPhone"
    }
    ```

    **Use Cases:**
    - Register device on app launch
    - Update token when FCM refreshes it
    - Re-register after app reinstall

    **Note:** If the token already exists, it will be updated with new device info.
    """

    notification_service = NotificationService(db)

    try:
        token = await notification_service.register_device(current_user, token_data)
        return NotificationTokenResponse.model_validate(token)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register device token: {str(e)}"
        )


@router.get("/tokens", response_model=List[NotificationTokenResponse])
async def list_device_tokens(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all registered device tokens for the current user

    Returns all active FCM tokens associated with your account.
    Useful for showing which devices are registered for notifications.

    **Returns:**
    List of registered devices

    **Example Response:**
    ```json
    [
      {
        "id": 1,
        "user_id": 123,
        "token": "fK7xJ...9pQm",
        "platform": "ios",
        "device_name": "iPhone 13 Pro",
        "is_active": true,
        "created_at": "2026-01-10T10:00:00Z",
        "last_used": "2026-01-13T15:30:00Z"
      },
      {
        "id": 2,
        "user_id": 123,
        "token": "dH9mK...2rTw",
        "platform": "android",
        "device_name": "Pixel 7",
        "is_active": true,
        "created_at": "2026-01-12T14:00:00Z",
        "last_used": "2026-01-13T14:20:00Z"
      }
    ]
    ```
    """

    notification_service = NotificationService(db)

    try:
        tokens = await notification_service.get_user_tokens(current_user)
        return [NotificationTokenResponse.model_validate(token) for token in tokens]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve device tokens: {str(e)}"
        )


@router.delete("/tokens/{token}", status_code=status.HTTP_200_OK)
async def unregister_device_token(
    token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Unregister a device token

    Removes the specified FCM token from your account.
    The device will no longer receive push notifications.

    **Path Parameters:**
    - **token**: FCM device token to remove

    **Returns:**
    Confirmation message

    **Example Response:**
    ```json
    {
      "message": "Device token unregistered successfully"
    }
    ```

    **Use Cases:**
    - User logs out from a specific device
    - Device is sold/given away
    - User wants to stop notifications on a device
    """

    notification_service = NotificationService(db)

    try:
        success = await notification_service.unregister_device(current_user, token)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device token not found"
            )

        return {"message": "Device token unregistered successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unregister device token: {str(e)}"
        )


@router.get("/preferences", response_model=NotificationPreferencesResponse)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get your notification preferences

    Returns your current notification settings including which types
    are enabled and quiet hours configuration.

    **Returns:**
    Notification preferences

    **Example Response:**
    ```json
    {
      "id": 1,
      "user_id": 123,
      "daily_affirmation": true,
      "reading_reminder": true,
      "journal_reminder": false,
      "moon_phase": true,
      "streak_milestone": true,
      "new_feature": true,
      "subscription_expiry": true,
      "quiet_hours_enabled": true,
      "quiet_hours_start": "22:00",
      "quiet_hours_end": "08:00",
      "created_at": "2026-01-10T10:00:00Z",
      "updated_at": "2026-01-13T10:00:00Z"
    }
    ```
    """

    notification_service = NotificationService(db)

    try:
        preferences = await notification_service.get_preferences(current_user)
        return NotificationPreferencesResponse.model_validate(preferences)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve notification preferences: {str(e)}"
        )


@router.put("/preferences", response_model=NotificationPreferencesResponse)
async def update_notification_preferences(
    preferences_update: NotificationPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update your notification preferences

    Configure which types of notifications you want to receive and
    set quiet hours when notifications should be silent.

    **Request Body (all fields optional):**
    - **daily_affirmation**: Enable/disable daily affirmations (morning)
    - **reading_reminder**: Enable/disable reading reminders
    - **journal_reminder**: Enable/disable journal reminders (evening)
    - **moon_phase**: Enable/disable moon phase updates (new/full moons)
    - **streak_milestone**: Enable/disable streak achievements
    - **new_feature**: Enable/disable new feature announcements
    - **subscription_expiry**: Enable/disable subscription expiry warnings
    - **quiet_hours_enabled**: Enable quiet hours mode
    - **quiet_hours_start**: Start time (24-hour format, e.g., "22:00")
    - **quiet_hours_end**: End time (24-hour format, e.g., "08:00")

    **Returns:**
    Updated preferences

    **Example:**
    ```json
    {
      "journal_reminder": false,
      "quiet_hours_enabled": true,
      "quiet_hours_start": "23:00",
      "quiet_hours_end": "07:00"
    }
    ```

    **Quiet Hours:**
    - No notifications sent during quiet hours
    - Supports overnight ranges (e.g., 22:00-08:00)
    - Time is based on UTC (adjust for user timezone in app)
    """

    notification_service = NotificationService(db)

    try:
        preferences = await notification_service.update_preferences(
            current_user,
            preferences_update
        )
        return NotificationPreferencesResponse.model_validate(preferences)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update notification preferences: {str(e)}"
        )


@router.post("/send", status_code=status.HTTP_200_OK)
async def send_test_notification(
    notification_data: NotificationSend,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a test notification (admin/testing only)

    Sends a custom notification to your registered devices.
    Useful for testing notification delivery.

    **Request Body:**
    - **notification_type**: Type of notification
    - **title**: Notification title (1-255 characters)
    - **body**: Notification message (1-1000 characters)
    - **data**: Optional additional data (JSON object)

    **Returns:**
    Send status

    **Example:**
    ```json
    {
      "notification_type": "custom",
      "title": "Test Notification",
      "body": "This is a test notification from Mystic.ai",
      "data": {
        "test_id": "123",
        "action": "open_app"
      }
    }
    ```

    **Note:** This endpoint respects user notification preferences.
    If user has disabled the notification type, it won't be sent.
    """

    notification_service = NotificationService(db)

    if not notification_service.is_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Push notifications are not configured. Check Firebase credentials."
        )

    try:
        success = await notification_service.send_notification(
            current_user,
            notification_data
        )

        if not success:
            return {
                "success": False,
                "message": "Notification not sent. Check user preferences or device registration."
            }

        return {
            "success": True,
            "message": "Notification sent successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send notification: {str(e)}"
        )


@router.get("/history", response_model=List[NotificationHistoryResponse])
async def get_notification_history(
    limit: int = Query(50, ge=1, le=100, description="Number of notifications to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get your notification history

    Returns a list of all notifications sent to you, including
    delivery status and timestamps.

    **Query Parameters:**
    - **limit**: Number of notifications to return (1-100, default: 50)
    - **offset**: Skip this many notifications for pagination (default: 0)

    **Returns:**
    List of notifications with delivery tracking

    **Example Response:**
    ```json
    [
      {
        "id": 1,
        "user_id": 123,
        "notification_type": "daily_affirmation",
        "title": "Your Daily Affirmation ✨",
        "body": "I trust my intuition to guide me...",
        "data": "{\\"type\\": \\"daily_affirmation\\"}",
        "sent": true,
        "delivered": true,
        "opened": false,
        "error_message": null,
        "created_at": "2026-01-13T08:00:00Z",
        "sent_at": "2026-01-13T08:00:01Z",
        "delivered_at": "2026-01-13T08:00:02Z",
        "opened_at": null
      }
    ]
    ```

    **Use Cases:**
    - View past notifications
    - Check delivery status
    - Debug notification issues
    - Track engagement metrics
    """

    notification_service = NotificationService(db)

    try:
        history = await notification_service.get_notification_history(
            current_user,
            limit=limit,
            offset=offset
        )

        return [NotificationHistoryResponse.model_validate(item) for item in history]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve notification history: {str(e)}"
        )


@router.post("/history/{notification_id}/opened", status_code=status.HTTP_200_OK)
async def mark_notification_opened(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a notification as opened

    Call this endpoint when user opens a notification in the app.
    Helps track engagement metrics.

    **Path Parameters:**
    - **notification_id**: ID of the notification from history

    **Returns:**
    Confirmation message

    **Example Response:**
    ```json
    {
      "message": "Notification marked as opened"
    }
    ```
    """

    notification_service = NotificationService(db)

    try:
        success = await notification_service.mark_notification_opened(
            notification_id,
            current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )

        return {"message": "Notification marked as opened"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark notification as opened: {str(e)}"
        )


@router.get("/status", status_code=status.HTTP_200_OK)
def get_notification_system_status():
    """
    Get push notification system status

    Returns whether push notifications are enabled and configured.

    **Returns:**
    System status

    **Example Response:**
    ```json
    {
      "enabled": true,
      "firebase_initialized": true,
      "message": "Push notifications are operational"
    }
    ```

    **Or (if not configured):**
    ```json
    {
      "enabled": false,
      "firebase_initialized": false,
      "message": "Push notifications are not configured"
    }
    ```
    """

    from app.services.notification_service import FIREBASE_AVAILABLE
    from app.db.session import SessionLocal

    db = SessionLocal()
    notification_service = NotificationService(db)
    db.close()

    enabled = notification_service.is_available()

    return {
        "enabled": enabled,
        "firebase_available": FIREBASE_AVAILABLE,
        "firebase_initialized": notification_service.firebase_initialized,
        "message": "Push notifications are operational" if enabled else "Push notifications are not configured"
    }
