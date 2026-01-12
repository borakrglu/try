"""
Database base configuration
"""

from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

# Import all models here for Alembic to detect them
from app.models.user import User  # noqa
from app.models.reading import Reading, ReadingImage  # noqa
from app.models.chat import ChatMessage  # noqa
from app.models.journal import JournalEntry  # noqa
from app.models.subscription import Subscription  # noqa
from app.models.user_stats import UserStats  # noqa
