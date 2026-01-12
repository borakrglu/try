"""
Reading Service - Business logic for mystical readings
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from app.models.reading import Reading, ReadingImage, ReadingType
from app.models.user import User
from app.schemas.reading import ReadingResponse
from app.ai.vision_service import VisionService
from app.ai.ai_service import AIService

logger = logging.getLogger(__name__)


class ReadingService:
    """Service for creating and managing readings"""

    def __init__(self, db: Session):
        self.db = db
        self.vision_service = VisionService()
        self.ai_service = AIService()

    async def create_coffee_reading(
        self,
        user: User,
        image_urls: List[str]
    ) -> Reading:
        """
        Create a coffee cup reading

        Args:
            user: Authenticated user
            image_urls: List of 3 image URLs [cup_interior, saucer, side_view]

        Returns:
            Created reading with AI-generated interpretation
        """
        logger.info(f"Creating coffee reading for user {user.id}")

        # Step 1: Analyze images with Vision AI
        all_symbols = []

        for idx, image_url in enumerate(image_urls):
            image_type = ["cup", "saucer", "side"][idx] if idx < 3 else "unknown"

            try:
                symbols = await self.vision_service.detect_coffee_symbols(
                    image_url=image_url,
                    image_type=image_type
                )
                all_symbols.extend(symbols)
            except Exception as e:
                logger.error(f"Vision analysis failed for image {idx}: {str(e)}")
                # Continue even if one image fails

        logger.info(f"Detected {len(all_symbols)} total symbols")

        # Step 2: Get user context
        zodiac_sign = user.zodiac_sign or "Unknown"
        recent_readings_summary = self._get_recent_readings_summary(user)
        moon_phase = self._get_current_moon_phase()

        # Step 3: Generate reading with AI
        reading_text, processing_time = await self.ai_service.generate_coffee_reading(
            user_name=user.name,
            zodiac_sign=zodiac_sign,
            symbols=all_symbols,
            language=user.language.value,
            moon_phase=moon_phase,
            recent_readings=recent_readings_summary
        )

        # Step 4: Save to database
        reading = Reading(
            user_id=user.id,
            type=ReadingType.COFFEE,
            input_data={
                "image_urls": image_urls,
                "moon_phase": moon_phase,
                "zodiac_sign": zodiac_sign
            },
            ai_response=reading_text,
            symbols_detected=all_symbols,
            processing_time_ms=processing_time,
        )

        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)

        # Step 5: Save image references
        for idx, image_url in enumerate(image_urls):
            image_type = ["cup", "saucer", "side"][idx] if idx < 3 else None

            reading_image = ReadingImage(
                reading_id=reading.id,
                image_url=image_url,
                image_type=image_type,
            )
            self.db.add(reading_image)

        self.db.commit()

        # Step 6: Update subscription usage counter
        user.subscription.readings_this_month += 1
        self.db.commit()

        # Step 7: Update user stats (gamification)
        if user.stats:
            user.stats.total_readings += 1
            user.stats.coffee_readings += 1
            user.stats.add_karma(25)  # 25 karma points for reading

            # Unlock badge if first coffee reading
            if user.stats.coffee_readings == 1:
                user.stats.unlock_badge("coffee_oracle")

            self.db.commit()

        logger.info(f"Coffee reading {reading.id} created successfully")

        return reading

    def get_reading_by_id(self, reading_id: int, user: User) -> Optional[Reading]:
        """
        Get a reading by ID (must belong to user)

        Args:
            reading_id: Reading ID
            user: Authenticated user

        Returns:
            Reading or None
        """
        reading = self.db.query(Reading).filter(
            Reading.id == reading_id,
            Reading.user_id == user.id
        ).first()

        return reading

    def get_user_readings(
        self,
        user: User,
        reading_type: Optional[ReadingType] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[Reading], int]:
        """
        Get user's readings with pagination

        Args:
            user: Authenticated user
            reading_type: Optional filter by type
            limit: Number of readings to return
            offset: Pagination offset

        Returns:
            Tuple of (readings, total_count)
        """
        query = self.db.query(Reading).filter(Reading.user_id == user.id)

        if reading_type:
            query = query.filter(Reading.type == reading_type)

        total = query.count()

        readings = query.order_by(Reading.created_at.desc()).limit(limit).offset(offset).all()

        return readings, total

    def rate_reading(
        self,
        reading_id: int,
        user: User,
        rating: int,
        feedback: Optional[str] = None
    ) -> Reading:
        """
        Rate a reading

        Args:
            reading_id: Reading ID
            user: Authenticated user
            rating: Rating (1-5)
            feedback: Optional feedback text

        Returns:
            Updated reading
        """
        reading = self.get_reading_by_id(reading_id, user)

        if not reading:
            raise ValueError("Reading not found")

        reading.rating = rating
        reading.feedback_text = feedback

        self.db.commit()
        self.db.refresh(reading)

        return reading

    def _get_recent_readings_summary(self, user: User, limit: int = 3) -> str:
        """Get summary of user's recent readings for context"""
        recent = self.db.query(Reading).filter(
            Reading.user_id == user.id
        ).order_by(Reading.created_at.desc()).limit(limit).all()

        if not recent:
            return "This is your first reading with Mystic.ai."

        summaries = []
        for r in recent:
            summaries.append(
                f"{r.type.value.capitalize()} reading on {r.created_at.strftime('%B %d')}"
            )

        return f"Recent activity: " + ", ".join(summaries)

    def _get_current_moon_phase(self) -> str:
        """
        Get current moon phase
        TODO: Implement real moon phase calculation or use API
        """
        # For now, return a static value
        # In production, use ephem library or astronomy API
        return "Waxing Crescent"
