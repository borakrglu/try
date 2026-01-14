"""
Gemini AI Service - Text generation with Google Gemini (FREE!)
Replacement for OpenAI GPT-4
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging
import time
import json

from app.config import settings
from app.ai.prompts.coffee_reading import get_coffee_reading_prompt
from app.ai.prompts.tarot_reading import get_tarot_reading_prompt, get_simple_tarot_prompt
from app.ai.prompts.palm_reading import get_palm_reading_prompt, get_simple_palm_prompt
from app.ai.tarot_spreads import format_spread_for_ai, get_spread, SpreadType

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for AI text generation using Google Gemini (FREE!)"""

    def __init__(self):
        """Initialize Gemini AI service"""
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Use Gemini 1.5 Flash - Fast and FREE!
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # For more complex tasks, use Gemini 1.5 Pro (still FREE but rate limited)
        self.pro_model = genai.GenerativeModel('gemini-1.5-pro')

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
        Generate coffee cup fortune reading using Gemini

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
        system_context = "You are a master Turkish coffee fortune teller, skilled in Tasseography."
        user_prompt = get_coffee_reading_prompt(
            user_name=user_name,
            zodiac_sign=zodiac_sign,
            symbols=symbols,
            language=language,
            moon_phase=moon_phase,
            recent_readings_summary=recent_readings
        )

        full_prompt = f"{system_context}\n\n{user_prompt}"

        logger.info(f"Generating coffee reading for {user_name} ({len(symbols)} symbols)")

        try:
            # Generate with Gemini
            response = await self._generate_async(
                prompt=full_prompt,
                temperature=0.8,  # Creative but coherent
                max_tokens=1200
            )

            reading_text = response.text
            processing_time = int((time.time() - start_time) * 1000)

            logger.info(f"Coffee reading generated: {len(reading_text)} chars in {processing_time}ms")

            return reading_text, processing_time

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
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
        Generate tarot card reading using Gemini

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
            system_context = "You are Mystic.ai's Master Tarot Reader, wise and intuitive, blending traditional tarot wisdom with modern psychological insight."
            user_prompt = get_simple_tarot_prompt(
                user_name=user_name,
                cards_data=cards,
                question=question,
                language=language
            )
            max_tokens = 800
        else:
            # Get spread description for context
            spread_info = f"{spread.name} - {spread.description}"

            system_context = "You are Mystic.ai's Master Tarot Reader, wise and intuitive, blending traditional tarot wisdom with modern psychological insight."
            user_prompt = get_tarot_reading_prompt(
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

        full_prompt = f"{system_context}\n\n{user_prompt}"

        try:
            response = await self._generate_async(
                prompt=full_prompt,
                temperature=0.8,  # Creative and intuitive
                max_tokens=max_tokens
            )

            reading_text = response.text
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
        language: str = "en",
        moon_phase: str = "Waxing Crescent",
        recent_readings: str = "This is the user's first palm reading."
    ) -> tuple[str, int]:
        """
        Generate palmistry reading using Gemini

        Args:
            user_name: User's name
            zodiac_sign: User's zodiac sign
            palm_data: Detected palm lines and features from Vision API
            hand_type: Type of hand (left, right)
            language: Output language
            moon_phase: Current moon phase
            recent_readings: Summary of recent readings

        Returns:
            Tuple of (reading_text, processing_time_ms)
        """
        start_time = time.time()

        logger.info(f"Generating palm reading for {user_name} ({hand_type} hand)")

        # Check if we have detailed palm data
        has_detailed_data = bool(palm_data.get("lines")) or bool(palm_data.get("hand_shape"))

        system_context = "You are Mystic.ai's Master Palmist, an expert in Chiromancy with deep knowledge of hand analysis and palm reading traditions worldwide."

        if has_detailed_data:
            # Use comprehensive prompt with detailed analysis
            user_prompt = get_palm_reading_prompt(
                user_name=user_name,
                zodiac_sign=zodiac_sign,
                palm_features=palm_data,
                hand_type=hand_type,
                language=language,
                moon_phase=moon_phase,
                recent_readings_summary=recent_readings
            )
            max_tokens = 1500
        else:
            # Use simplified prompt when detailed features aren't available
            user_prompt = get_simple_palm_prompt(
                user_name=user_name,
                hand_type=hand_type,
                palm_features=palm_data,
                language=language
            )
            max_tokens = 800

        full_prompt = f"{system_context}\n\n{user_prompt}"

        try:
            response = await self._generate_async(
                prompt=full_prompt,
                temperature=0.7,  # Balanced between consistency and creativity
                max_tokens=max_tokens
            )

            reading_text = response.text
            processing_time = int((time.time() - start_time) * 1000)

            logger.info(f"Palm reading generated: {len(reading_text)} chars in {processing_time}ms")

            return reading_text, processing_time

        except Exception as e:
            logger.error(f"Palm reading error: {str(e)}")
            raise

    async def _generate_async(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Any:
        """
        Generate text with Gemini (async wrapper)

        Args:
            prompt: Text prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Gemini response object
        """
        # Gemini generation config
        generation_config = {
            'temperature': temperature,
            'max_output_tokens': max_tokens,
            'top_p': 0.95,
            'top_k': 40
        }

        # Generate content
        # Note: Gemini Python SDK doesn't have native async yet,
        # so we'll use asyncio to wrap the sync call
        import asyncio
        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None,
            lambda: self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
        )

        return response
