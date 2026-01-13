"""
AI prompts package
"""

from app.ai.prompts.coffee_reading import get_coffee_reading_prompt
from app.ai.prompts.tarot_reading import get_tarot_reading_prompt
from app.ai.prompts.palm_reading import get_palm_reading_prompt
from app.ai.prompts.chat_personas import (
    get_sage_prompt,
    get_witch_prompt,
    get_astrologer_prompt,
    get_persona_prompt,
    get_system_context
)
from app.ai.prompts.journal_analysis import (
    get_sentiment_analysis_prompt,
    get_affirmation_prompt,
    get_dream_interpretation_prompt,
    get_mood_trend_analysis_prompt
)

__all__ = [
    "get_coffee_reading_prompt",
    "get_tarot_reading_prompt",
    "get_palm_reading_prompt",
    "get_sage_prompt",
    "get_witch_prompt",
    "get_astrologer_prompt",
    "get_persona_prompt",
    "get_system_context",
    "get_sentiment_analysis_prompt",
    "get_affirmation_prompt",
    "get_dream_interpretation_prompt",
    "get_mood_trend_analysis_prompt",
]
