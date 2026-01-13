"""
Astrology API endpoints - Moon phases and astrological data
"""

from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional

from app.services.moon_phase import MoonPhaseService

router = APIRouter()
moon_service = MoonPhaseService()


@router.get("/moon/current")
def get_current_moon_phase():
    """
    Get current moon phase and lunar data

    Returns comprehensive information about the current moon phase including:
    - Phase name (New Moon, Waxing Crescent, First Quarter, etc.)
    - Illumination percentage (0-100%)
    - Moon's zodiac sign
    - Days until next full moon and new moon
    - Spiritual meaning and energy of current phase
    - Recommended crystals and rituals

    **Returns:**
    Complete moon phase data with spiritual guidance

    **Example Response:**
    ```json
    {
      "phase_name": "Waxing Crescent",
      "phase_key": "waxing_crescent",
      "emoji": "🌒",
      "illumination": 23.4,
      "cycle_position": 0.125,
      "days_to_full_moon": 11.2,
      "days_to_new_moon": 25.8,
      "moon_sign": "Taurus",
      "date": "2026-01-13T10:00:00Z",
      "meaning": {
        "energy": "Growth, Building Momentum",
        "themes": ["Taking action", "Building foundation", "Nurturing growth"],
        "guidance": "Take first steps toward your goals...",
        "chakra_focus": "Solar Plexus, Sacral",
        "crystal": "Citrine, Carnelian",
        "ritual": "Create a vision board, practice daily affirmations..."
      }
    }
    ```

    **Use Cases:**
    - Display moon phase in app header
    - Provide daily lunar guidance
    - Recommend rituals based on phase
    - Inform chat persona responses (The Astrologer)
    - Contextualize readings with lunar energy
    """

    return moon_service.get_current_phase()


@router.get("/moon/phase")
def get_moon_phase_for_date(
    date: Optional[str] = Query(None, description="Date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
):
    """
    Get moon phase for a specific date

    **Query Parameters:**
    - **date**: Date in ISO format (e.g., "2026-01-13" or "2026-01-13T10:00:00")
                If not provided, returns current moon phase

    **Returns:**
    Moon phase data for the specified date

    **Example:**
    - `/api/v1/astrology/moon/phase?date=2026-01-15`
    - Returns moon phase for January 15, 2026
    """

    if date:
        try:
            # Parse date string
            if "T" in date:
                parsed_date = datetime.fromisoformat(date.replace("Z", "+00:00"))
            else:
                parsed_date = datetime.fromisoformat(date)

            return moon_service.get_current_phase(parsed_date)
        except ValueError:
            return {
                "error": "Invalid date format. Use ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS"
            }
    else:
        return moon_service.get_current_phase()


@router.get("/moon/calendar/{year}/{month}")
def get_lunar_calendar(
    year: int = Query(..., ge=2020, le=2030, description="Year"),
    month: int = Query(..., ge=1, le=12, description="Month (1-12)")
):
    """
    Get lunar calendar for a specific month

    Shows all new moons and full moons in the specified month with their zodiac signs.

    **Path Parameters:**
    - **year**: Year (2020-2030)
    - **month**: Month (1-12)

    **Returns:**
    List of new moons and full moons with dates and zodiac signs

    **Example Response:**
    ```json
    {
      "year": 2026,
      "month": 1,
      "new_moons": [
        {
          "date": "2026-01-06",
          "moon_sign": "Capricorn"
        }
      ],
      "full_moons": [
        {
          "date": "2026-01-21",
          "moon_sign": "Leo"
        }
      ]
    }
    ```

    **Use Cases:**
    - Plan rituals around lunar events
    - Display lunar calendar in app
    - Remind users of upcoming full/new moons
    - Recommend best times for manifestation work
    """

    return moon_service.get_lunar_calendar(year, month)


@router.get("/transits")
def get_current_transits():
    """
    Get current astrological transits

    Returns a human-readable summary of current astrological conditions
    including moon phase, seasonal energy, and general cosmic guidance.

    **Note:** This is a simplified transit system. It includes moon phase
    and seasonal energies. For precise planetary positions, consider
    integrating with a dedicated astrology API in production.

    **Returns:**
    Transit summary string

    **Example Response:**
    ```json
    {
      "summary": "Moon in Taurus (Waxing Crescent), Spring renewal energy flows through March. Focus on growth and building momentum.",
      "moon_phase": "Waxing Crescent",
      "moon_sign": "Taurus",
      "season": "Spring",
      "date": "2026-03-15T10:00:00Z"
    }
    ```

    **Use Cases:**
    - Provide context for The Astrologer chat persona
    - Add astrological context to daily affirmations
    - Inform reading interpretations
    - Display on home screen as daily cosmic weather
    """

    moon_data = moon_service.get_current_phase()
    transit_summary = moon_service.get_astrological_transits()

    # Determine season
    month = datetime.now().month
    if month in [3, 4, 5]:
        season = "Spring"
    elif month in [6, 7, 8]:
        season = "Summer"
    elif month in [9, 10, 11]:
        season = "Autumn"
    else:
        season = "Winter"

    return {
        "summary": transit_summary,
        "moon_phase": moon_data["phase_name"],
        "moon_sign": moon_data["moon_sign"],
        "season": season,
        "date": datetime.now().isoformat()
    }


@router.get("/zodiac/compatibility")
def get_zodiac_compatibility(
    sign1: str = Query(..., description="First zodiac sign"),
    sign2: str = Query(..., description="Second zodiac sign")
):
    """
    Get compatibility between two zodiac signs

    **Query Parameters:**
    - **sign1**: First zodiac sign (e.g., "aries", "taurus")
    - **sign2**: Second zodiac sign (e.g., "leo", "pisces")

    **Returns:**
    Compatibility rating and insights

    **Example:**
    `/api/v1/astrology/zodiac/compatibility?sign1=leo&sign2=sagittarius`

    **Example Response:**
    ```json
    {
      "sign1": "Leo",
      "sign2": "Sagittarius",
      "compatibility_score": 9,
      "rating": "Excellent Match",
      "element_match": "Fire + Fire",
      "summary": "This is a dynamic, passionate pairing...",
      "strengths": ["Shared enthusiasm", "Adventurous spirits", "Natural chemistry"],
      "challenges": ["Both want to lead", "Can be impulsive", "Need for independence"]
    }
    ```

    **Note:** This is a simplified compatibility system based on elements
    and traditional zodiac relationships. For detailed synastry, consider
    birth chart analysis.
    """

    # Normalize signs
    sign1 = sign1.lower().capitalize()
    sign2 = sign2.lower().capitalize()

    zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    if sign1 not in zodiac_signs or sign2 not in zodiac_signs:
        return {
            "error": f"Invalid zodiac sign. Must be one of: {', '.join(zodiac_signs)}"
        }

    # Element mapping
    elements = {
        "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
        "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
        "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
        "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
    }

    element1 = elements[sign1]
    element2 = elements[sign2]

    # Calculate compatibility (simplified)
    if element1 == element2:
        score = 8
        rating = "Excellent Match"
        summary = f"Both {element1} signs share similar energy and values."
    elif (element1 in ["Fire", "Air"] and element2 in ["Fire", "Air"]) or \
         (element1 in ["Earth", "Water"] and element2 in ["Earth", "Water"]):
        score = 7
        rating = "Good Match"
        summary = f"{element1} and {element2} complement each other well."
    else:
        score = 5
        rating = "Moderate Match"
        summary = f"{element1} and {element2} bring different energies that require understanding."

    return {
        "sign1": sign1,
        "sign2": sign2,
        "compatibility_score": score,
        "rating": rating,
        "element_match": f"{element1} + {element2}",
        "summary": summary,
        "strengths": ["Unique perspectives", "Growth opportunities", "Balancing energies"],
        "challenges": ["Different communication styles", "Need for compromise", "Understanding differences"]
    }


@router.get("/moon/ritual-guide")
def get_ritual_guide():
    """
    Get ritual recommendations based on current moon phase

    Returns specific ritual suggestions, crystals, and practices
    aligned with the current lunar energy.

    **Returns:**
    Ritual guide for current moon phase

    **Example Response:**
    ```json
    {
      "current_phase": "Full Moon",
      "emoji": "🌕",
      "best_for": ["Release", "Manifestation", "Charging crystals"],
      "ritual_suggestions": [
        {
          "name": "Full Moon Release Ceremony",
          "duration": "30 minutes",
          "items_needed": ["Paper", "Fireproof bowl", "Matches", "Pen"],
          "steps": [
            "Write down what you want to release",
            "Read it aloud under the moon",
            "Burn the paper safely",
            "Express gratitude for the lesson"
          ]
        },
        {
          "name": "Moon Water Creation",
          "duration": "Overnight",
          "items_needed": ["Glass jar", "Spring water"],
          "steps": [
            "Fill jar with clean water",
            "Place under direct moonlight",
            "Leave overnight",
            "Use for plants, cleansing, or drinking"
          ]
        }
      ],
      "crystals_to_charge": ["Selenite", "Moonstone", "Labradorite", "Clear Quartz"],
      "journaling_prompts": [
        "What am I ready to release?",
        "What lessons did I learn this lunar cycle?",
        "What am I grateful for?"
      ]
    }
    ```

    **Use Cases:**
    - Provide daily ritual recommendations
    - Educate users about moon magic
    - Enhance engagement with lunar cycles
    - Content for The Witch persona
    """

    moon_data = moon_service.get_current_phase()
    meaning = moon_data["meaning"]

    # Build ritual guide
    ritual_guide = {
        "current_phase": moon_data["phase_name"],
        "emoji": moon_data["emoji"],
        "illumination": moon_data["illumination"],
        "energy": meaning["energy"],
        "best_for": meaning["themes"],
        "guidance": meaning["guidance"],
        "chakra_focus": meaning["chakra_focus"],
        "recommended_crystals": meaning["crystal"].split(", "),
        "ritual": meaning["ritual"],
        "journaling_prompts": _get_journaling_prompts(moon_data["phase_key"])
    }

    return ritual_guide


def _get_journaling_prompts(phase_key: str) -> list:
    """Get journaling prompts for specific moon phase"""
    prompts = {
        "new_moon": [
            "What intentions am I setting for this lunar cycle?",
            "What new beginning am I ready to embrace?",
            "What does my ideal life look like 6 months from now?"
        ],
        "waxing_crescent": [
            "What small steps can I take today toward my goals?",
            "Where do I need to build more momentum?",
            "What habits will support my intentions?"
        ],
        "first_quarter": [
            "What obstacles am I facing right now?",
            "What decision have I been avoiding?",
            "How can I push through resistance with grace?"
        ],
        "waxing_gibbous": [
            "What adjustments do I need to make?",
            "Where am I being called to have patience?",
            "What is almost ready to manifest?"
        ],
        "full_moon": [
            "What am I ready to release?",
            "What lessons did I learn this cycle?",
            "What am I celebrating and grateful for?"
        ],
        "waning_gibbous": [
            "What wisdom can I share with others?",
            "How can I give back to my community?",
            "What am I grateful for today?"
        ],
        "last_quarter": [
            "What patterns am I ready to let go of?",
            "Who or what do I need to forgive (including myself)?",
            "What emotional baggage can I release?"
        ],
        "waning_crescent": [
            "How can I rest more deeply?",
            "What did I learn from this lunar cycle?",
            "How am I preparing for new beginnings?"
        ]
    }

    return prompts.get(phase_key, prompts["new_moon"])
