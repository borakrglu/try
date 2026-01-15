"""
AI Factory - Provider-agnostic AI service selection
Automatically selects Gemini (FREE!) or OpenAI based on configuration
"""

from typing import Any
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class AIFactory:
    """
    Factory for creating AI service instances based on configuration

    Supports:
    - Gemini (FREE! - Default)
    - OpenAI (Paid - Fallback)
    """

    _text_service_instance = None
    _vision_service_instance = None

    @classmethod
    def get_text_service(cls) -> Any:
        """
        Get text generation service (for readings, chat, journal)

        Returns:
            AI service instance (GeminiService or AIService)
        """
        if cls._text_service_instance is None:
            provider = settings.AI_PROVIDER.lower()

            if provider == "gemini":
                try:
                    from app.ai.gemini_service import GeminiService
                    cls._text_service_instance = GeminiService()
                    logger.info("✅ Using Gemini AI (FREE!) for text generation")
                except Exception as e:
                    logger.error(f"Failed to initialize Gemini: {e}")
                    try:
                        from app.ai.ai_service import AIService
                        cls._text_service_instance = AIService()
                        logger.info("Using OpenAI GPT-4 for text generation (fallback)")
                    except ImportError:
                        raise RuntimeError("Neither Gemini nor OpenAI are available. Install google-generativeai or openai package.")

            elif provider == "openai":
                from app.ai.ai_service import AIService
                cls._text_service_instance = AIService()
                logger.info("Using OpenAI GPT-4 for text generation")

            else:
                logger.warning(f"Unknown AI provider: {provider}. Defaulting to Gemini.")
                from app.ai.gemini_service import GeminiService
                cls._text_service_instance = GeminiService()
                logger.info("✅ Using Gemini AI (FREE!) for text generation (default)")

        return cls._text_service_instance

    @classmethod
    def get_vision_service(cls) -> Any:
        """
        Get vision/image analysis service (for coffee/palm readings)

        Returns:
            Vision service instance (GeminiVisionService or VisionService)
        """
        if cls._vision_service_instance is None:
            provider = settings.AI_PROVIDER.lower()

            if provider == "gemini":
                try:
                    from app.ai.gemini_vision import GeminiVisionService
                    cls._vision_service_instance = GeminiVisionService()
                    logger.info("✅ Using Gemini Vision (FREE!) for image analysis")
                except Exception as e:
                    logger.error(f"Failed to initialize Gemini Vision: {e}")
                    try:
                        from app.ai.vision_service import VisionService
                        cls._vision_service_instance = VisionService()
                        logger.info("Using OpenAI GPT-4 Vision for image analysis (fallback)")
                    except ImportError:
                        raise RuntimeError("Neither Gemini Vision nor OpenAI Vision are available. Install google-generativeai or openai package.")

            elif provider == "openai":
                from app.ai.vision_service import VisionService
                cls._vision_service_instance = VisionService()
                logger.info("Using OpenAI GPT-4 Vision for image analysis")

            else:
                logger.warning(f"Unknown AI provider: {provider}. Defaulting to Gemini.")
                from app.ai.gemini_vision import GeminiVisionService
                cls._vision_service_instance = GeminiVisionService()
                logger.info("✅ Using Gemini Vision (FREE!) for image analysis (default)")

        return cls._vision_service_instance

    @classmethod
    def reset(cls):
        """Reset cached instances (useful for testing or provider switching)"""
        cls._text_service_instance = None
        cls._vision_service_instance = None
        logger.info("AI Factory reset - instances cleared")


# Convenience functions
def get_ai_service() -> Any:
    """Get the configured text generation AI service"""
    return AIFactory.get_text_service()


def get_vision_service() -> Any:
    """Get the configured vision/image analysis service"""
    return AIFactory.get_vision_service()
