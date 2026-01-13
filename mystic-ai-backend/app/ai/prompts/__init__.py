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

__all__ = [
    "get_coffee_reading_prompt",
    "get_tarot_reading_prompt",
    "get_palm_reading_prompt",
    "get_sage_prompt",
    "get_witch_prompt",
    "get_astrologer_prompt",
    "get_persona_prompt",
    "get_system_context",
]
