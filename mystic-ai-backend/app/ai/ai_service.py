"""
AI Service - Text generation with OpenAI GPT-4
"""

from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional
import logging
import time

from app.config import settings
from app.ai.prompts.coffee_reading import get_coffee_reading_prompt
from app.ai.prompts.tarot_reading import get_tarot_reading_prompt, get_simple_tarot_prompt
from app.ai.tarot_spreads import format_spread_for_ai, get_spread, SpreadType

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI text generation using OpenAI GPT-4"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_coffee_reading(
        self,
        user_name: str,
        zodiac_sign: str,
        symbols: List[Dict[str, Any]],
        language: str = "en",
        moon_phase: str = "Waxing Crescent",
        recent_readings: str = "This is the user's first reading."
    ) -> tuple[str, int]:
        """
        Generate coffee cup fortune reading

        Args:
            user_name: User's name
            zodiac_sign: User's zodiac sign
            symbols: Detected symbols from Vision API
            language: Output language (en, tr, de)
            moon_phase: Current moon phase
            recent_readings: Summary of recent readings

        Returns:
            Tuple of (reading_text, processing_time_ms)
        """
        start_time = time.time()

        # Build prompt
        prompt = get_coffee_reading_prompt(
            user_name=user_name,
            zodiac_sign=zodiac_sign,
            symbols=symbols,
            language=language,
            moon_phase=moon_phase,
            recent_readings_summary=recent_readings
        )

        logger.info(f"Generating coffee reading for {user_name} ({len(symbols)} symbols)")

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master Turkish coffee fortune teller, skilled in Tasseography."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Creative but coherent
                max_tokens=1200,  # Enough for 600-800 words
            )

            reading_text = response.choices[0].message.content
            processing_time = int((time.time() - start_time) * 1000)

            logger.info(f"Coffee reading generated: {len(reading_text)} chars in {processing_time}ms")

            return reading_text, processing_time

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    async def generate_tarot_reading(
        self,
        user_name: str,
        zodiac_sign: str,
        cards: List[Dict[str, Any]],
        spread_type: str,
        question: Optional[str] = None,
        language: str = "en",
        moon_phase: str = "Waxing Crescent",
        recent_readings: str = "This is the user's first tarot reading."
    ) -> tuple[str, int]:
        """
        Generate tarot card reading

        Args:
            user_name: User's name
            zodiac_sign: User's zodiac sign
            cards: Selected tarot cards with positions
            spread_type: Type of spread (single, three_card, celtic_cross, etc.)
            question: Optional user question
            language: Output language
            moon_phase: Current moon phase
            recent_readings: Summary of recent readings

        Returns:
            Tuple of (reading_text, processing_time_ms)
        """
        start_time = time.time()

        # Convert spread_type string to enum if needed
        try:
            spread_enum = SpreadType(spread_type.lower())
        except ValueError:
            spread_enum = SpreadType.THREE_CARD  # Default fallback

        # Get spread information
        spread = get_spread(spread_enum)

        # Format cards for AI prompt
        cards_formatted = format_spread_for_ai(spread_enum, cards)

        # Use question or default based on spread
        if not question:
            question = f"General guidance using {spread.name}"

        logger.info(f"Generating tarot reading for {user_name} ({spread.name}, {len(cards)} cards)")

        # Choose prompt based on complexity
        if len(cards) <= 3:
            prompt = get_simple_tarot_prompt(
                user_name=user_name,
                cards_data=cards,
                question=question,
                language=language
            )
            max_tokens = 800
        else:
            # Get spread description for context
            spread_info = f"{spread.name} - {spread.description}"

            prompt = get_tarot_reading_prompt(
                user_name=user_name,
                zodiac_sign=zodiac_sign,
                question=question,
                spread_info=spread_info,
                cards_formatted=cards_formatted,
                language=language,
                moon_phase=moon_phase,
                recent_readings_summary=recent_readings
            )
            max_tokens = 1500

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Mystic.ai's Master Tarot Reader, wise and intuitive, blending traditional tarot wisdom with modern psychological insight."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Creative and intuitive
                max_tokens=max_tokens,
            )

            reading_text = response.choices[0].message.content
            processing_time = int((time.time() - start_time) * 1000)

            logger.info(f"Tarot reading generated: {len(reading_text)} chars in {processing_time}ms")

            return reading_text, processing_time

        except Exception as e:
            logger.error(f"Tarot reading error: {str(e)}")
            raise

    async def generate_palm_reading(
        self,
        user_name: str,
        zodiac_sign: str,
        palm_data: Dict[str, Any],
        hand_type: str,
        language: str = "en"
    ) -> tuple[str, int]:
        """
        Generate palmistry reading

        Args:
            user_name: User's name
            zodiac_sign: User's zodiac sign
            palm_data: Detected palm lines and features
            hand_type: Type of hand (left, right)
            language: Output language

        Returns:
            Tuple of (reading_text, processing_time_ms)
        """
        start_time = time.time()

        # TODO: Implement palm reading prompt
        prompt = f"Generate a palmistry reading for {user_name}..."

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a palmistry expert."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1200,
            )

            reading_text = response.choices[0].message.content
            processing_time = int((time.time() - start_time) * 1000)

            return reading_text, processing_time

        except Exception as e:
            logger.error(f"Palm reading error: {str(e)}")
            raise

    async def analyze_journal_sentiment(
        self,
        content: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of journal entry

        Args:
            content: Journal entry text
            language: Entry language

        Returns:
            Sentiment analysis results
        """
        # TODO: Implement sentiment analysis
        return {
            "primary_emotion": "neutral",
            "energy_level": 5,
            "stress_indicators": [],
            "positive_aspects": []
        }

    async def generate_affirmation(
        self,
        mood: str,
        chakra_imbalances: List[str],
        zodiac_sign: str,
        language: str = "en"
    ) -> str:
        """
        Generate personalized affirmation

        Args:
            mood: Current mood
            chakra_imbalances: List of weak chakras
            zodiac_sign: User's zodiac sign
            language: Output language

        Returns:
            Affirmation text
        """
        # TODO: Implement affirmation generation
        return "I am capable, worthy, and open to the opportunities that come my way."
