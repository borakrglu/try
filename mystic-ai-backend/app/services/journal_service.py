"""
Journal Service - Manage journal entries with AI-powered insights
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import time
import logging
import json

from openai import AsyncOpenAI

from app.models.journal import JournalEntry
from app.models.user import User
from app.models.user_stats import UserStats
from app.schemas.journal import (
    JournalEntryCreate,
    JournalEntryUpdate,
    JournalEntryResponse,
    JournalInsightsResponse,
    ChakraInsights,
    MoodInsights,
    MoodCalendarDay,
    MoodCalendarResponse
)
from app.config import settings
from app.ai.prompts.journal_analysis import (
    get_sentiment_analysis_prompt,
    get_affirmation_prompt,
    get_dream_interpretation_prompt,
    get_mood_trend_analysis_prompt
)

logger = logging.getLogger(__name__)


class JournalService:
    """
    Service for managing journal entries with AI-powered analysis

    Features:
    - Sentiment analysis with emotional tone detection
    - Chakra energy scoring (7 chakras, 1-10 scale)
    - Personalized affirmation generation
    - Dream symbol interpretation
    - Mood trend analysis and streak tracking
    """

    def __init__(self, db: Session):
        """
        Initialize journal service

        Args:
            db: Database session
        """
        self.db = db
        self.ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def create_entry(
        self,
        user: User,
        entry_data: JournalEntryCreate,
        analyze: bool = True
    ) -> JournalEntry:
        """
        Create a new journal entry with optional AI analysis

        Args:
            user: User object
            entry_data: Journal entry data
            analyze: Whether to perform AI analysis (default: True)

        Returns:
            Created journal entry with analysis
        """
        start_time = time.time()

        # Create entry
        entry = JournalEntry(
            user_id=user.id,
            content=entry_data.content,
            entry_type=entry_data.entry_type,
            mood=entry_data.mood,
            tags=entry_data.tags
        )

        logger.info(f"Creating {entry_data.entry_type} entry for user {user.id} ({len(entry_data.content)} chars)")

        # Perform AI analysis if requested
        if analyze and entry_data.entry_type != "gratitude":  # Skip analysis for gratitude lists
            try:
                # Get sentiment and chakra analysis
                sentiment_data, chakra_scores = await self._analyze_sentiment(entry_data.content)

                entry.sentiment_analysis = sentiment_data
                entry.chakra_scores = chakra_scores

                # Generate personalized affirmation
                affirmation = await self._generate_affirmation(
                    sentiment_data=sentiment_data,
                    chakra_scores=chakra_scores,
                    user_name=user.name,
                    zodiac_sign=user.zodiac_sign or "Unknown",
                    language=user.language.value
                )
                entry.generated_affirmation = affirmation

                logger.info(f"AI analysis completed in {int((time.time() - start_time) * 1000)}ms")

            except Exception as e:
                logger.error(f"AI analysis failed: {str(e)}")
                # Continue without analysis - entry is still saved

        # Save to database
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)

        # Update user stats and streaks
        await self._update_user_stats(user)

        total_time = int((time.time() - start_time) * 1000)
        logger.info(f"Journal entry {entry.id} created in {total_time}ms")

        return entry

    async def _analyze_sentiment(self, content: str) -> tuple[Dict[str, Any], Dict[str, int]]:
        """
        Analyze sentiment and chakra scores using AI

        Args:
            content: Journal entry text

        Returns:
            Tuple of (sentiment_data, chakra_scores)
        """

        prompt = get_sentiment_analysis_prompt(content)

        try:
            response = await self.ai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a sentiment analysis expert specializing in emotional intelligence and chakra energy systems. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Low temperature for consistent analysis
                max_tokens=800,
            )

            # Parse JSON response
            analysis_json = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if analysis_json.startswith("```"):
                analysis_json = analysis_json.split("```json")[1].split("```")[0].strip()
            elif analysis_json.startswith("```"):
                analysis_json = analysis_json.strip("`").strip()

            analysis = json.loads(analysis_json)

            # Extract sentiment data and chakra scores
            sentiment_data = {
                "primary_emotion": analysis.get("primary_emotion", "neutral"),
                "energy_level": analysis.get("energy_level", 5),
                "stress_indicators": analysis.get("stress_indicators", []),
                "positive_aspects": analysis.get("positive_aspects", []),
                "affirmation_themes": analysis.get("affirmation_themes", []),
                "summary": analysis.get("summary", "")
            }

            chakra_scores = analysis.get("chakra_analysis", {
                "root": 5,
                "sacral": 5,
                "solar_plexus": 5,
                "heart": 5,
                "throat": 5,
                "third_eye": 5,
                "crown": 5
            })

            return sentiment_data, chakra_scores

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse sentiment analysis JSON: {e}")
            # Return default values
            return self._get_default_sentiment(), self._get_default_chakras()

        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return self._get_default_sentiment(), self._get_default_chakras()

    def _get_default_sentiment(self) -> Dict[str, Any]:
        """Get default sentiment data when analysis fails"""
        return {
            "primary_emotion": "neutral",
            "energy_level": 5,
            "stress_indicators": [],
            "positive_aspects": [],
            "affirmation_themes": ["self_love", "peace"],
            "summary": "Journal entry recorded"
        }

    def _get_default_chakras(self) -> Dict[str, int]:
        """Get default chakra scores when analysis fails"""
        return {
            "root": 5,
            "sacral": 5,
            "solar_plexus": 5,
            "heart": 5,
            "throat": 5,
            "third_eye": 5,
            "crown": 5
        }

    async def _generate_affirmation(
        self,
        sentiment_data: Dict[str, Any],
        chakra_scores: Dict[str, int],
        user_name: str,
        zodiac_sign: str,
        language: str
    ) -> str:
        """
        Generate personalized affirmation

        Args:
            sentiment_data: Sentiment analysis results
            chakra_scores: Chakra scores
            user_name: User's name
            zodiac_sign: User's zodiac sign
            language: Output language

        Returns:
            Affirmation text
        """

        prompt = get_affirmation_prompt(
            sentiment_data=sentiment_data,
            chakra_scores=chakra_scores,
            user_name=user_name,
            zodiac_sign=zodiac_sign,
            language=language
        )

        try:
            response = await self.ai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert affirmation writer. Create powerful, personalized affirmations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Creative but not random
                max_tokens=100,
            )

            affirmation = response.choices[0].message.content.strip()

            # Clean up any quotes or extra formatting
            affirmation = affirmation.strip('"').strip("'").strip()

            return affirmation

        except Exception as e:
            logger.error(f"Affirmation generation error: {e}")
            # Return a default affirmation
            return "I am exactly where I need to be on my journey."

    async def _update_user_stats(self, user: User) -> None:
        """
        Update user statistics and journal streaks

        Args:
            user: User object
        """

        stats = self.db.query(UserStats).filter(UserStats.user_id == user.id).first()

        if not stats:
            logger.warning(f"No stats found for user {user.id}")
            return

        # Increment journal entries count
        stats.journal_entries += 1

        # Update streak
        today = datetime.utcnow().date()
        last_journal_date = stats.last_journal_date.date() if stats.last_journal_date else None

        if last_journal_date:
            days_since_last = (today - last_journal_date).days

            if days_since_last == 0:
                # Same day - no streak change
                pass
            elif days_since_last == 1:
                # Consecutive day - increment streak
                stats.current_journal_streak += 1
                if stats.current_journal_streak > stats.longest_journal_streak:
                    stats.longest_journal_streak = stats.current_journal_streak
            else:
                # Streak broken - reset to 1
                stats.current_journal_streak = 1
        else:
            # First journal entry
            stats.current_journal_streak = 1
            stats.longest_journal_streak = 1

        stats.last_journal_date = datetime.utcnow()
        stats.last_active = datetime.utcnow()

        # Award karma points
        karma_awarded = 10
        if stats.current_journal_streak >= 7:
            karma_awarded += 50  # Bonus for 7-day streak

        stats.karma_points += karma_awarded

        self.db.commit()

        logger.info(f"User {user.id} stats updated: streak={stats.current_journal_streak}, karma=+{karma_awarded}")

    async def get_entries(
        self,
        user: User,
        entry_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[JournalEntry]:
        """
        Get user's journal entries

        Args:
            user: User object
            entry_type: Filter by type (optional)
            limit: Number of entries to return
            offset: Pagination offset

        Returns:
            List of journal entries
        """

        query = self.db.query(JournalEntry).filter(JournalEntry.user_id == user.id)

        if entry_type:
            query = query.filter(JournalEntry.entry_type == entry_type)

        entries = (
            query
            .order_by(JournalEntry.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return entries

    async def get_entry_by_id(self, user: User, entry_id: int) -> Optional[JournalEntry]:
        """Get a single journal entry by ID"""
        return (
            self.db.query(JournalEntry)
            .filter(JournalEntry.id == entry_id, JournalEntry.user_id == user.id)
            .first()
        )

    async def update_entry(
        self,
        user: User,
        entry_id: int,
        update_data: JournalEntryUpdate
    ) -> Optional[JournalEntry]:
        """Update a journal entry"""

        entry = await self.get_entry_by_id(user, entry_id)

        if not entry:
            return None

        # Update fields
        if update_data.content is not None:
            entry.content = update_data.content
        if update_data.mood is not None:
            entry.mood = update_data.mood
        if update_data.tags is not None:
            entry.tags = update_data.tags

        entry.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(entry)

        return entry

    async def delete_entry(self, user: User, entry_id: int) -> bool:
        """Delete a journal entry"""

        entry = await self.get_entry_by_id(user, entry_id)

        if not entry:
            return False

        self.db.delete(entry)
        self.db.commit()

        return True

    async def get_insights(self, user: User) -> Dict[str, Any]:
        """
        Get comprehensive journal insights for user

        Args:
            user: User object

        Returns:
            Journal insights with chakra balance, mood trends, streaks
        """

        # Get recent entries (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_entries = (
            self.db.query(JournalEntry)
            .filter(
                JournalEntry.user_id == user.id,
                JournalEntry.created_at >= seven_days_ago
            )
            .order_by(JournalEntry.created_at.desc())
            .all()
        )

        # Calculate average chakra scores
        if recent_entries:
            chakra_totals = {
                "root": 0, "sacral": 0, "solar_plexus": 0,
                "heart": 0, "throat": 0, "third_eye": 0, "crown": 0
            }
            count = 0

            for entry in recent_entries:
                if entry.chakra_scores:
                    count += 1
                    for chakra, score in entry.chakra_scores.items():
                        chakra_totals[chakra] += score

            if count > 0:
                chakra_balance = {k: int(v / count) for k, v in chakra_totals.items()}
            else:
                chakra_balance = self._get_default_chakras()
        else:
            chakra_balance = self._get_default_chakras()

        # Calculate mood insights
        energy_levels = [e.sentiment_analysis.get("energy_level", 5) for e in recent_entries if e.sentiment_analysis]
        avg_energy = int(sum(energy_levels) / len(energy_levels)) if energy_levels else 5

        emotions = [e.sentiment_analysis.get("primary_emotion", "neutral") for e in recent_entries if e.sentiment_analysis]
        dominant_emotion = max(set(emotions), key=emotions.count) if emotions else "neutral"

        # Mood trend
        if len(energy_levels) >= 3:
            recent_avg = sum(energy_levels[:3]) / 3
            older_avg = sum(energy_levels[3:]) / len(energy_levels[3:]) if len(energy_levels) > 3 else recent_avg

            if recent_avg > older_avg + 1:
                mood_trend = "improving"
            elif recent_avg < older_avg - 1:
                mood_trend = "declining"
            else:
                mood_trend = "stable"
        else:
            mood_trend = "stable"

        # Get user stats for streak
        stats = self.db.query(UserStats).filter(UserStats.user_id == user.id).first()
        journal_streak = stats.current_journal_streak if stats else 0
        total_entries = stats.journal_entries if stats else 0

        # Generate affirmation of the day
        if recent_entries and recent_entries[0].sentiment_analysis and recent_entries[0].chakra_scores:
            affirmation = recent_entries[0].generated_affirmation or "You are exactly where you need to be."
        else:
            affirmation = "I embrace today with an open heart and clear mind."

        return {
            "chakra_balance": chakra_balance,
            "mood_insights": {
                "current_mood": recent_entries[0].mood if recent_entries else None,
                "energy_level": avg_energy,
                "stress_level": 10 - avg_energy,  # Inverse of energy
                "dominant_emotion": dominant_emotion,
                "mood_trend": mood_trend
            },
            "journal_streak": journal_streak,
            "total_entries": total_entries,
            "affirmation_of_the_day": affirmation
        }

    async def get_mood_calendar(
        self,
        user: User,
        year: int,
        month: int
    ) -> MoodCalendarResponse:
        """
        Get mood calendar for a specific month

        Args:
            user: User object
            year: Year
            month: Month (1-12)

        Returns:
            Mood calendar with daily mood/energy data
        """

        # Get all entries for the month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        entries = (
            self.db.query(JournalEntry)
            .filter(
                JournalEntry.user_id == user.id,
                JournalEntry.created_at >= start_date,
                JournalEntry.created_at < end_date
            )
            .all()
        )

        # Group by date
        entries_by_date = {}
        for entry in entries:
            date_key = entry.created_at.date()
            if date_key not in entries_by_date:
                entries_by_date[date_key] = entry
            # Keep only the first entry of the day for calendar view

        # Build calendar days
        days = []
        current_date = start_date.date()
        while current_date < end_date.date():
            entry = entries_by_date.get(current_date)

            day_data = MoodCalendarDay(
                date=datetime.combine(current_date, datetime.min.time()),
                mood=entry.mood if entry else None,
                energy_level=entry.sentiment_analysis.get("energy_level") if entry and entry.sentiment_analysis else None,
                has_entry=entry is not None
            )

            days.append(day_data)
            current_date += timedelta(days=1)

        return MoodCalendarResponse(
            year=year,
            month=month,
            days=days
        )
