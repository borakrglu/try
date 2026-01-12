"""
Zodiac sign calculator
"""

from datetime import datetime
from typing import Optional


def calculate_zodiac_sign(birth_date: datetime) -> str:
    """
    Calculate zodiac sign from birth date

    Args:
        birth_date: User's birth date

    Returns:
        Zodiac sign name
    """
    day = birth_date.day
    month = birth_date.month

    # Zodiac date ranges
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:  # (month == 2 and day >= 19) or (month == 3 and day <= 20)
        return "Pisces"


def get_zodiac_element(zodiac_sign: str) -> str:
    """
    Get the element for a zodiac sign

    Args:
        zodiac_sign: Zodiac sign name

    Returns:
        Element (Fire, Earth, Air, Water)
    """
    elements = {
        "Aries": "Fire",
        "Leo": "Fire",
        "Sagittarius": "Fire",
        "Taurus": "Earth",
        "Virgo": "Earth",
        "Capricorn": "Earth",
        "Gemini": "Air",
        "Libra": "Air",
        "Aquarius": "Air",
        "Cancer": "Water",
        "Scorpio": "Water",
        "Pisces": "Water",
    }
    return elements.get(zodiac_sign, "Unknown")


def get_zodiac_traits(zodiac_sign: str) -> dict:
    """
    Get personality traits for a zodiac sign

    Args:
        zodiac_sign: Zodiac sign name

    Returns:
        Dictionary with traits
    """
    traits = {
        "Aries": {
            "strengths": ["Courageous", "Determined", "Confident", "Enthusiastic"],
            "weaknesses": ["Impatient", "Moody", "Short-tempered"],
        },
        "Taurus": {
            "strengths": ["Reliable", "Patient", "Practical", "Devoted"],
            "weaknesses": ["Stubborn", "Possessive", "Uncompromising"],
        },
        "Gemini": {
            "strengths": ["Gentle", "Affectionate", "Curious", "Adaptable"],
            "weaknesses": ["Nervous", "Inconsistent", "Indecisive"],
        },
        "Cancer": {
            "strengths": ["Tenacious", "Loyal", "Emotional", "Sympathetic"],
            "weaknesses": ["Moody", "Pessimistic", "Suspicious"],
        },
        "Leo": {
            "strengths": ["Creative", "Passionate", "Generous", "Cheerful"],
            "weaknesses": ["Arrogant", "Stubborn", "Self-centered"],
        },
        "Virgo": {
            "strengths": ["Loyal", "Analytical", "Kind", "Hardworking"],
            "weaknesses": ["Shyness", "Worry", "Overly critical"],
        },
        "Libra": {
            "strengths": ["Cooperative", "Diplomatic", "Gracious", "Fair-minded"],
            "weaknesses": ["Indecisive", "Avoids confrontations", "Self-pity"],
        },
        "Scorpio": {
            "strengths": ["Resourceful", "Brave", "Passionate", "Stubborn"],
            "weaknesses": ["Distrusting", "Jealous", "Secretive"],
        },
        "Sagittarius": {
            "strengths": ["Generous", "Idealistic", "Great sense of humor"],
            "weaknesses": ["Impatient", "Says anything no matter how undiplomatic"],
        },
        "Capricorn": {
            "strengths": ["Responsible", "Disciplined", "Self-control", "Good managers"],
            "weaknesses": ["Know-it-all", "Unforgiving", "Condescending"],
        },
        "Aquarius": {
            "strengths": ["Progressive", "Original", "Independent", "Humanitarian"],
            "weaknesses": ["Runs from emotional expression", "Temperamental", "Uncompromising"],
        },
        "Pisces": {
            "strengths": ["Compassionate", "Artistic", "Intuitive", "Gentle"],
            "weaknesses": ["Fearful", "Overly trusting", "Sad", "Desire to escape reality"],
        },
    }
    return traits.get(zodiac_sign, {"strengths": [], "weaknesses": []})
