"""
Tarot Spread Layouts - Different spread configurations for readings
"""

from typing import List, Dict
from enum import Enum


class SpreadType(str, Enum):
    """Available tarot spread types"""
    SINGLE_CARD = "single_card"
    THREE_CARD = "three_card"
    CELTIC_CROSS = "celtic_cross"
    HORSESHOE = "horseshoe"
    RELATIONSHIP = "relationship"
    CAREER = "career"


class TarotSpread:
    """Represents a tarot spread layout"""

    def __init__(
        self,
        name: str,
        spread_type: SpreadType,
        card_count: int,
        positions: List[Dict[str, str]],
        description: str,
        best_for: List[str]
    ):
        self.name = name
        self.spread_type = spread_type
        self.card_count = card_count
        self.positions = positions  # [{"position": 1, "meaning": "Past", "description": "..."}]
        self.description = description
        self.best_for = best_for


# Define all spread layouts
SPREADS = {
    SpreadType.SINGLE_CARD: TarotSpread(
        name="Single Card",
        spread_type=SpreadType.SINGLE_CARD,
        card_count=1,
        positions=[
            {
                "position": 1,
                "meaning": "Insight",
                "description": "Direct answer or guidance for your question"
            }
        ],
        description="A single card draw for quick guidance or daily insight",
        best_for=["Daily guidance", "Quick yes/no questions", "Daily meditation"]
    ),

    SpreadType.THREE_CARD: TarotSpread(
        name="Three Card Spread",
        spread_type=SpreadType.THREE_CARD,
        card_count=3,
        positions=[
            {
                "position": 1,
                "meaning": "Past",
                "description": "Past influences affecting the current situation"
            },
            {
                "position": 2,
                "meaning": "Present",
                "description": "Current situation and energies at play"
            },
            {
                "position": 3,
                "meaning": "Future",
                "description": "Potential outcome or future direction"
            }
        ],
        description="Classic past-present-future spread for understanding the timeline of a situation",
        best_for=["General questions", "Understanding timeline", "Quick comprehensive reading"]
    ),

    SpreadType.CELTIC_CROSS: TarotSpread(
        name="Celtic Cross",
        spread_type=SpreadType.CELTIC_CROSS,
        card_count=10,
        positions=[
            {
                "position": 1,
                "meaning": "Present Situation",
                "description": "The heart of the matter, your current circumstances"
            },
            {
                "position": 2,
                "meaning": "Challenge/Crossing",
                "description": "What crosses you - obstacles or opposing forces"
            },
            {
                "position": 3,
                "meaning": "Foundation",
                "description": "The basis of the situation, root cause, or distant past"
            },
            {
                "position": 4,
                "meaning": "Recent Past",
                "description": "What is passing or just behind you"
            },
            {
                "position": 5,
                "meaning": "Crown/Best Outcome",
                "description": "What crowns you - your goal or best possible outcome"
            },
            {
                "position": 6,
                "meaning": "Near Future",
                "description": "What is approaching in the immediate future"
            },
            {
                "position": 7,
                "meaning": "Your Approach",
                "description": "Your attitude, how you see yourself in this situation"
            },
            {
                "position": 8,
                "meaning": "External Influences",
                "description": "How others see you, external environment"
            },
            {
                "position": 9,
                "meaning": "Hopes and Fears",
                "description": "Your hopes, dreams, or underlying fears"
            },
            {
                "position": 10,
                "meaning": "Final Outcome",
                "description": "The culmination, final result if current path continues"
            }
        ],
        description="Comprehensive 10-card spread providing deep insight into complex situations",
        best_for=["Complex situations", "Life-changing decisions", "Deep introspection"]
    ),

    SpreadType.HORSESHOE: TarotSpread(
        name="Horseshoe Spread",
        spread_type=SpreadType.HORSESHOE,
        card_count=7,
        positions=[
            {
                "position": 1,
                "meaning": "Past",
                "description": "Past influences and experiences"
            },
            {
                "position": 2,
                "meaning": "Present",
                "description": "Current situation and energies"
            },
            {
                "position": 3,
                "meaning": "Hidden Influences",
                "description": "Unknown factors affecting the situation"
            },
            {
                "position": 4,
                "meaning": "Obstacles",
                "description": "Challenges to overcome"
            },
            {
                "position": 5,
                "meaning": "External Influences",
                "description": "Environmental factors and other people"
            },
            {
                "position": 6,
                "meaning": "Advice",
                "description": "Guidance on what to do"
            },
            {
                "position": 7,
                "meaning": "Outcome",
                "description": "Likely outcome if advice is followed"
            }
        ],
        description="Seven-card spread shaped like a horseshoe for balanced guidance",
        best_for=["Decision making", "Seeking advice", "Understanding influences"]
    ),

    SpreadType.RELATIONSHIP: TarotSpread(
        name="Relationship Spread",
        spread_type=SpreadType.RELATIONSHIP,
        card_count=7,
        positions=[
            {
                "position": 1,
                "meaning": "You",
                "description": "Your position in the relationship"
            },
            {
                "position": 2,
                "meaning": "The Other Person",
                "description": "Their position in the relationship"
            },
            {
                "position": 3,
                "meaning": "Connection",
                "description": "The energy binding you together"
            },
            {
                "position": 4,
                "meaning": "Your Needs",
                "description": "What you need from this relationship"
            },
            {
                "position": 5,
                "meaning": "Their Needs",
                "description": "What they need from this relationship"
            },
            {
                "position": 6,
                "meaning": "Challenges",
                "description": "Obstacles or areas needing attention"
            },
            {
                "position": 7,
                "meaning": "Potential",
                "description": "Where this relationship is headed"
            }
        ],
        description="Specialized spread for understanding romantic or platonic relationships",
        best_for=["Relationship questions", "Understanding connection", "Partnership issues"]
    ),

    SpreadType.CAREER: TarotSpread(
        name="Career Path Spread",
        spread_type=SpreadType.CAREER,
        card_count=5,
        positions=[
            {
                "position": 1,
                "meaning": "Current Career Situation",
                "description": "Where you stand now professionally"
            },
            {
                "position": 2,
                "meaning": "Your Strengths",
                "description": "Skills and talents to leverage"
            },
            {
                "position": 3,
                "meaning": "Obstacles",
                "description": "Challenges in your career path"
            },
            {
                "position": 4,
                "meaning": "Opportunities",
                "description": "Potential opportunities to explore"
            },
            {
                "position": 5,
                "meaning": "Advice",
                "description": "Guidance for career advancement"
            }
        ],
        description="Five-card spread focused on career and professional development",
        best_for=["Career decisions", "Job changes", "Professional growth"]
    )
}


def get_spread(spread_type: SpreadType) -> TarotSpread:
    """Get a specific spread by type"""
    if spread_type not in SPREADS:
        raise ValueError(f"Spread type '{spread_type}' not found")
    return SPREADS[spread_type]


def get_all_spreads() -> Dict[SpreadType, TarotSpread]:
    """Get all available spreads"""
    return SPREADS


def get_spread_description(spread_type: SpreadType) -> str:
    """Get a formatted description of a spread"""
    spread = get_spread(spread_type)

    description = f"""
**{spread.name}** ({spread.card_count} cards)

{spread.description}

**Best for:** {', '.join(spread.best_for)}

**Positions:**
"""
    for pos in spread.positions:
        description += f"\n{pos['position']}. **{pos['meaning']}**: {pos['description']}"

    return description


def format_spread_for_ai(
    spread_type: SpreadType,
    cards_data: List[Dict]
) -> str:
    """
    Format spread and card data for AI prompt

    Args:
        spread_type: Type of spread used
        cards_data: List of card dictionaries with position info

    Returns:
        Formatted string for AI consumption
    """
    spread = get_spread(spread_type)

    formatted = f"SPREAD: {spread.name}\n\n"

    for i, card_data in enumerate(cards_data):
        position = spread.positions[i]
        card = card_data['card']

        formatted += f"""
Position {position['position']}: {position['meaning']}
- {position['description']}
- Card: {card['name']} ({card['suit']})
- Orientation: {'Reversed' if card['reversed'] else 'Upright'}
- Keywords: {', '.join(card['keywords'])}
- Meaning: {card['meaning']}

"""

    return formatted
