"""
Pydantic schemas for Journal
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any


# Journal entry schemas
class JournalEntryCreate(BaseModel):
    """Schema for creating a journal entry"""
    content: str = Field(..., min_length=1, max_length=10000)
    entry_type: str = Field(default="journal", pattern="^(journal|dream|gratitude)$")
    mood: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None


class JournalEntryUpdate(BaseModel):
    """Schema for updating a journal entry"""
    content: Optional[str] = Field(None, min_length=1, max_length=10000)
    mood: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None


class JournalEntryResponse(BaseModel):
    """Schema for journal entry in API responses"""
    id: int
    user_id: int
    content: str
    entry_type: str
    mood: Optional[str] = None
    tags: Optional[List[str]] = None
    sentiment_analysis: Optional[Dict[str, Any]] = None
    chakra_scores: Optional[Dict[str, int]] = None
    generated_affirmation: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Insights schemas
class ChakraInsights(BaseModel):
    """Chakra balance insights"""
    root: int = Field(..., ge=0, le=10)
    sacral: int = Field(..., ge=0, le=10)
    solar_plexus: int = Field(..., ge=0, le=10)
    heart: int = Field(..., ge=0, le=10)
    throat: int = Field(..., ge=0, le=10)
    third_eye: int = Field(..., ge=0, le=10)
    crown: int = Field(..., ge=0, le=10)


class MoodInsights(BaseModel):
    """Mood trends and insights"""
    current_mood: Optional[str] = None
    energy_level: int = Field(..., ge=0, le=10)
    stress_level: int = Field(..., ge=0, le=10)
    dominant_emotion: Optional[str] = None
    mood_trend: str  # improving, declining, stable


class JournalInsightsResponse(BaseModel):
    """Combined journal insights"""
    chakra_balance: ChakraInsights
    mood_insights: MoodInsights
    journal_streak: int
    total_entries: int
    affirmation_of_the_day: str


# Calendar view
class MoodCalendarDay(BaseModel):
    """Mood for a single day"""
    date: datetime
    mood: Optional[str] = None
    energy_level: Optional[int] = None
    has_entry: bool


class MoodCalendarResponse(BaseModel):
    """Mood calendar for a month"""
    year: int
    month: int
    days: List[MoodCalendarDay]
