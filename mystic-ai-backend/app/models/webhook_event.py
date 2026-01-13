"""
Webhook Event Model - Transaction logging for webhooks
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from datetime import datetime

from app.db.base import Base


class WebhookEvent(Base):
    """
    Webhook event model - logs all incoming webhooks for audit trail
    """
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)

    # Webhook metadata
    source = Column(String(50), nullable=False, index=True)  # 'revenuecat', 'stripe', etc.
    event_type = Column(String(100), nullable=False, index=True)  # 'INITIAL_PURCHASE', 'RENEWAL', etc.
    event_id = Column(String(255), unique=True, nullable=True, index=True)  # External event ID

    # User association
    user_id = Column(Integer, nullable=True, index=True)  # May be null if user not found

    # Event data
    payload = Column(JSON, nullable=False)  # Full webhook payload

    # Processing status
    processed = Column(Boolean, default=False, nullable=False, index=True)
    processed_at = Column(DateTime, nullable=True)
    error_message = Column(String(500), nullable=True)

    # Request metadata
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(255), nullable=True)

    # Timestamps
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<WebhookEvent(id={self.id}, source={self.source}, type={self.event_type}, processed={self.processed})>"

    def mark_as_processed(self):
        """Mark webhook as successfully processed"""
        self.processed = True
        self.processed_at = datetime.utcnow()

    def mark_as_failed(self, error: str):
        """Mark webhook as failed with error message"""
        self.processed = False
        self.error_message = error[:500]  # Truncate long error messages
