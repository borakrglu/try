"""
Moon Phase Service - Calculate lunar phases and astrological data

Provides real-time moon phase calculation and basic astrological transit information
for use in readings, chat personas, and journal insights.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Tuple
import math


class MoonPhaseService:
    """
    Service for calculating moon phases and providing lunar insights

    Uses astronomical calculations based on the lunar synodic month (29.53 days)
    to determine current moon phase without external API dependencies.
    """

    # Known new moon reference point (January 6, 2000, 18:14 UTC)
    KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)

    # Lunar cycle length in days (synodic month)
    LUNAR_CYCLE = 29.53058867

    # Moon phase names and their ranges (percentage of cycle)
    MOON_PHASES = [
        (0.0, 0.033, "New Moon", "🌑", "new_moon"),
        (0.033, 0.216, "Waxing Crescent", "🌒", "waxing_crescent"),
        (0.216, 0.284, "First Quarter", "🌓", "first_quarter"),
        (0.284, 0.466, "Waxing Gibbous", "🌔", "waxing_gibbous"),
        (0.466, 0.534, "Full Moon", "🌕", "full_moon"),
        (0.534, 0.716, "Waning Gibbous", "🌖", "waning_gibbous"),
        (0.716, 0.784, "Last Quarter", "🌗", "last_quarter"),
        (0.784, 0.967, "Waning Crescent", "🌘", "waning_crescent"),
        (0.967, 1.0, "New Moon", "🌑", "new_moon"),
    ]

    def get_current_phase(self, date: datetime = None) -> Dict[str, Any]:
        """
        Get current moon phase data

        Args:
            date: Date to calculate for (default: now)

        Returns:
            Dictionary with moon phase information
        """
        if date is None:
            date = datetime.now(timezone.utc)
        elif date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

        # Calculate days since known new moon
        delta = date - self.KNOWN_NEW_MOON
        days_since_new_moon = delta.total_seconds() / 86400

        # Calculate position in current lunar cycle (0.0 to 1.0)
        cycle_position = (days_since_new_moon % self.LUNAR_CYCLE) / self.LUNAR_CYCLE

        # Determine phase name
        phase_name, emoji, phase_key = self._get_phase_name(cycle_position)

        # Calculate illumination percentage
        illumination = self._calculate_illumination(cycle_position)

        # Calculate days until next full moon and new moon
        days_to_full = self._days_until_phase(cycle_position, 0.5)
        days_to_new = self._days_until_phase(cycle_position, 0.0)

        # Get moon sign (simplified zodiac position)
        moon_sign = self._get_moon_sign(date)

        # Get phase meaning and energy
        meaning = self._get_phase_meaning(phase_key)

        return {
            "phase_name": phase_name,
            "phase_key": phase_key,
            "emoji": emoji,
            "illumination": round(illumination, 1),
            "cycle_position": round(cycle_position, 3),
            "days_to_full_moon": round(days_to_full, 1),
            "days_to_new_moon": round(days_to_new, 1),
            "moon_sign": moon_sign,
            "date": date.isoformat(),
            "meaning": meaning
        }

    def _get_phase_name(self, cycle_position: float) -> Tuple[str, str, str]:
        """
        Get phase name and emoji based on cycle position

        Args:
            cycle_position: Position in cycle (0.0 to 1.0)

        Returns:
            Tuple of (phase_name, emoji, phase_key)
        """
        for start, end, name, emoji, key in self.MOON_PHASES:
            if start <= cycle_position < end:
                return name, emoji, key

        # Default to New Moon if somehow outside range
        return "New Moon", "🌑", "new_moon"

    def _calculate_illumination(self, cycle_position: float) -> float:
        """
        Calculate moon illumination percentage

        Args:
            cycle_position: Position in cycle (0.0 to 1.0)

        Returns:
            Illumination percentage (0-100)
        """
        # Illumination follows a cosine curve
        # 0.0 (new) = 0%, 0.5 (full) = 100%, 1.0 (new) = 0%
        illumination = (1 - math.cos(2 * math.pi * cycle_position)) / 2
        return illumination * 100

    def _days_until_phase(self, current_position: float, target_position: float) -> float:
        """
        Calculate days until a specific phase

        Args:
            current_position: Current cycle position (0.0 to 1.0)
            target_position: Target phase position (0.0 to 1.0)

        Returns:
            Days until target phase
        """
        if target_position >= current_position:
            days = (target_position - current_position) * self.LUNAR_CYCLE
        else:
            days = (1.0 - current_position + target_position) * self.LUNAR_CYCLE

        return days

    def _get_moon_sign(self, date: datetime) -> str:
        """
        Get approximate moon zodiac sign

        Simplified calculation: Moon moves through zodiac in ~27.3 days
        This is an approximation and not astronomically precise.

        Args:
            date: Date to calculate for

        Returns:
            Zodiac sign name
        """
        # Zodiac signs
        zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]

        # Known reference: Moon was in Taurus on Jan 1, 2000
        reference_date = datetime(2000, 1, 1, tzinfo=timezone.utc)
        reference_sign_index = 1  # Taurus

        # Calculate days since reference
        delta = date - reference_date
        days = delta.total_seconds() / 86400

        # Moon moves through zodiac in ~27.3 days (sidereal month)
        sidereal_month = 27.321661
        signs_per_day = 12 / sidereal_month

        # Calculate current sign
        sign_offset = int(days * signs_per_day)
        current_sign_index = (reference_sign_index + sign_offset) % 12

        return zodiac_signs[current_sign_index]

    def _get_phase_meaning(self, phase_key: str) -> Dict[str, Any]:
        """
        Get spiritual meaning and energy of moon phase

        Args:
            phase_key: Phase key identifier

        Returns:
            Dictionary with meaning, energy, and recommendations
        """
        meanings = {
            "new_moon": {
                "energy": "New Beginnings, Intention Setting",
                "themes": ["Fresh starts", "Planting seeds", "Manifesting intentions"],
                "guidance": "Set intentions, start new projects, journal your goals for this lunar cycle.",
                "chakra_focus": "Third Eye, Crown",
                "crystal": "Clear Quartz, Moonstone",
                "ritual": "Write intentions on paper, light a white candle, meditate on your desires."
            },
            "waxing_crescent": {
                "energy": "Growth, Building Momentum",
                "themes": ["Taking action", "Building foundation", "Nurturing growth"],
                "guidance": "Take first steps toward your goals, build positive habits, stay committed.",
                "chakra_focus": "Solar Plexus, Sacral",
                "crystal": "Citrine, Carnelian",
                "ritual": "Create a vision board, practice daily affirmations, plant actual seeds or herbs."
            },
            "first_quarter": {
                "energy": "Action, Overcoming Obstacles",
                "themes": ["Challenges arise", "Decision making", "Perseverance"],
                "guidance": "Push through resistance, make decisions, adjust your plans as needed.",
                "chakra_focus": "Solar Plexus, Root",
                "crystal": "Tiger's Eye, Red Jasper",
                "ritual": "Identify one obstacle and create an action plan, practice courage-building breathwork."
            },
            "waxing_gibbous": {
                "energy": "Refinement, Patience",
                "themes": ["Fine-tuning", "Patience", "Trust the process"],
                "guidance": "Refine your approach, stay patient, trust that manifestation is near.",
                "chakra_focus": "Heart, Throat",
                "crystal": "Rose Quartz, Amazonite",
                "ritual": "Review your progress, adjust course if needed, practice gratitude for growth."
            },
            "full_moon": {
                "energy": "Manifestation, Release, Illumination",
                "themes": ["Peak power", "Clarity", "Letting go"],
                "guidance": "Celebrate manifestations, release what no longer serves you, charge crystals under moonlight.",
                "chakra_focus": "All chakras (full activation)",
                "crystal": "Selenite, Labradorite",
                "ritual": "Full moon bath, write what to release and burn it, moon water creation, crystal charging."
            },
            "waning_gibbous": {
                "energy": "Gratitude, Sharing Wisdom",
                "themes": ["Giving back", "Teaching", "Gratitude"],
                "guidance": "Share what you've learned, express gratitude, help others on their journey.",
                "chakra_focus": "Heart, Throat",
                "crystal": "Aventurine, Lapis Lazuli",
                "ritual": "Write a gratitude list, share your knowledge, donate or volunteer."
            },
            "last_quarter": {
                "energy": "Release, Forgiveness",
                "themes": ["Letting go", "Forgiveness", "Clearing space"],
                "guidance": "Release old patterns, forgive yourself and others, clear physical and emotional clutter.",
                "chakra_focus": "Heart, Third Eye",
                "crystal": "Black Tourmaline, Amethyst",
                "ritual": "Cord-cutting meditation, clean and declutter your space, journaling about what to release."
            },
            "waning_crescent": {
                "energy": "Rest, Reflection, Surrender",
                "themes": ["Inner work", "Rest", "Preparation"],
                "guidance": "Rest deeply, reflect on the cycle, prepare for the next new moon, practice self-care.",
                "chakra_focus": "Crown, Root",
                "crystal": "Smoky Quartz, Amethyst",
                "ritual": "Restorative yoga, meditation, salt bath, early bedtime, reflect on lessons learned."
            }
        }

        return meanings.get(phase_key, meanings["new_moon"])

    def get_lunar_calendar(self, year: int, month: int) -> Dict[str, Any]:
        """
        Get lunar calendar for a specific month

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            Dictionary with key lunar events for the month
        """
        # Find new moons and full moons in the month
        start_date = datetime(year, month, 1, tzinfo=timezone.utc)

        if month == 12:
            end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            end_date = datetime(year, month + 1, 1, tzinfo=timezone.utc)

        new_moons = []
        full_moons = []

        # Check each day of the month
        current = start_date
        previous_phase_key = None

        while current < end_date:
            phase_data = self.get_current_phase(current)
            phase_key = phase_data["phase_key"]

            # Detect transitions
            if phase_key == "new_moon" and previous_phase_key != "new_moon":
                new_moons.append({
                    "date": current.date().isoformat(),
                    "moon_sign": phase_data["moon_sign"]
                })
            elif phase_key == "full_moon" and previous_phase_key != "full_moon":
                full_moons.append({
                    "date": current.date().isoformat(),
                    "moon_sign": phase_data["moon_sign"]
                })

            previous_phase_key = phase_key
            current = current.replace(day=current.day + 1)

        return {
            "year": year,
            "month": month,
            "new_moons": new_moons,
            "full_moons": full_moons
        }

    def get_astrological_transits(self, date: datetime = None) -> str:
        """
        Get simplified astrological transits for chat context

        This is a simplified version. In production, you'd use an astronomy API
        or library like skyfield for accurate planetary positions.

        Args:
            date: Date to calculate for (default: now)

        Returns:
            Human-readable transit summary
        """
        if date is None:
            date = datetime.now(timezone.utc)

        moon_data = self.get_current_phase(date)

        # Create a contextual transit summary
        month_name = date.strftime("%B")
        day = date.day

        transit_summary = f"Moon in {moon_data['moon_sign']} ({moon_data['phase_name']}), "

        # Add seasonal context
        month = date.month
        if month in [3, 4, 5]:
            transit_summary += f"Spring renewal energy flows through {month_name}. "
        elif month in [6, 7, 8]:
            transit_summary += f"Summer manifestation energy peaks in {month_name}. "
        elif month in [9, 10, 11]:
            transit_summary += f"Autumn reflection energy deepens in {month_name}. "
        else:
            transit_summary += f"Winter introspection energy guides {month_name}. "

        # Add moon phase guidance
        phase_meaning = moon_data["meaning"]
        transit_summary += f"Focus on {phase_meaning['energy'].lower()}."

        return transit_summary
