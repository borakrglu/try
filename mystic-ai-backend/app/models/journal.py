"""
Journal entry model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class JournalEntry(Base):
    """
    Journal entry model - stores user's daily journal entries
    """
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Entry content
    content = Column(Text, nullable=False)

    # Entry type (journal, dream, gratitude)
    entry_type = Column(String(50), default="journal", nullable=False)

    # User-selected mood (emoji or text)
    mood = Column(String(50), nullable=True)

    # Tags (work, love, family, health, etc.)
    tags = Column(ARRAY(String), nullable=True)

    # AI sentiment analysis results (JSON)
    # {
    #   "primary_emotion": "joy",
    #   "energy_level": 7,
    #   "stress_indicators": ["work pressure"],
    #   "positive_aspects": ["gratitude"]
    # }
    sentiment_analysis = Column(JSON, nullable=True)

    # Chakra scores (JSON)
    # {
    #   "root": 7,
    #   "sacral": 5,
    #   "solar_plexus": 6,
    #   "heart": 8,
    #   "throat": 7,
    #   "third_eye": 6,
    #   "crown": 5
    # }
    chakra_scores = Column(JSON, nullable=True)

    # AI-generated affirmation based on this entry
    generated_affirmation = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    user = relationship("User", back_populates="journal_entries")

    def __repr__(self):
        return f"<JournalEntry(id={self.id}, user_id={self.user_id}, type={self.entry_type}, created_at={self.created_at})>"
