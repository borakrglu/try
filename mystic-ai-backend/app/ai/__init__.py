"""
AI package - Vision and text generation services
"""

# Import Gemini services (always available)
from app.ai.ai_factory import AIFactory
from app.ai.gemini_service import GeminiService
from app.ai.gemini_vision import GeminiVisionService

# OpenAI services are optional (only if openai package installed)
try:
    from app.ai.vision_service import VisionService
    from app.ai.ai_service import AIService
    _openai_available = True
except ImportError:
    VisionService = None
    AIService = None
    _openai_available = False

__all__ = [
    "AIFactory",
    "GeminiService",
    "GeminiVisionService",
    "VisionService",
    "AIService",
]
