"""
User statistics model - for gamification
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class UserStats(Base):
    """
    User statistics model - tracks karma points, badges, streaks
    """
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)

    # Karma points (earned through various actions)
    karma_points = Column(Integer, default=0, nullable=False, index=True)

    # Activity counters
    total_readings = Column(Integer, default=0, nullable=False)
    coffee_readings = Column(Integer, default=0, nullable=False)
    tarot_readings = Column(Integer, default=0, nullable=False)
    palm_readings = Column(Integer, default=0, nullable=False)
    chat_messages_sent = Column(Integer, default=0, nullable=False)
    journal_entries = Column(Integer, default=0, nullable=False)

    # Streaks
    current_journal_streak = Column(Integer, default=0, nullable=False)
    longest_journal_streak = Column(Integer, default=0, nullable=False)
    last_journal_date = Column(DateTime, nullable=True)

    # Badges (JSON array)
    # ["mystic_novice", "dream_keeper", "card_master", etc.]
    badges = Column(JSON, default=list, nullable=False)

    # Last activity timestamp
    last_active = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Daily quest completion (JSON)
    # {
    #   "2026-01-12": ["daily_card", "journal_entry", "chat_sage"],
    #   "2026-01-13": ["daily_card"]
    # }
    daily_quests = Column(JSON, default=dict, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    user = relationship("User", back_populates="stats")

    def __repr__(self):
        return f"<UserStats(user_id={self.user_id}, karma={self.karma_points}, badges={len(self.badges)})>"

    def add_karma(self, points: int) -> int:
        """Add karma points and return new total"""
        self.karma_points += points
        return self.karma_points

    def unlock_badge(self, badge_name: str) -> bool:
        """Unlock a badge if not already unlocked"""
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            return True
        return False

    def has_badge(self, badge_name: str) -> bool:
        """Check if user has a specific badge"""
        return badge_name in self.badges

    def update_journal_streak(self) -> int:
        """Update journal streak and return current streak"""
        today = datetime.utcnow().date()

        if not self.last_journal_date:
            # First entry
            self.current_journal_streak = 1
            self.longest_journal_streak = 1
        else:
            last_date = self.last_journal_date.date()
            days_diff = (today - last_date).days

            if days_diff == 0:
                # Already journaled today, no change
                pass
            elif days_diff == 1:
                # Consecutive day, increase streak
                self.current_journal_streak += 1
                if self.current_journal_streak > self.longest_journal_streak:
                    self.longest_journal_streak = self.current_journal_streak
            else:
                # Streak broken, reset
                self.current_journal_streak = 1

        self.last_journal_date = datetime.utcnow()
        return self.current_journal_streak
