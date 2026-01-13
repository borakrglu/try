"""
API v1 routes
"""

from app.api.v1 import auth, readings, upload, webhooks, chat, journal, astrology, notifications, admin, analytics

__all__ = ["auth", "readings", "upload", "webhooks", "chat", "journal", "astrology", "notifications", "admin", "analytics"]
