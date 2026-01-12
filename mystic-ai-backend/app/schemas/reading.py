"""
Pydantic schemas for Readings
"""

from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.models.reading import ReadingType


# Coffee Reading Schemas
class CoffeeReadingCreate(BaseModel):
    """Schema for creating a coffee reading"""
    # Images will be uploaded separately, this receives S3 URLs
    cup_image_url: HttpUrl
    saucer_image_url: HttpUrl
    side_image_url: HttpUrl


# Tarot Reading Schemas
class TarotCard(BaseModel):
    """Single tarot card"""
    name: str
    position: int
    reversed: bool = False


class TarotReadingCreate(BaseModel):
    """Schema for creating a tarot reading"""
    spread_type: str = Field(..., regex="^(single|three_card|celtic_cross|relationship|career)$")
    cards: List[TarotCard]
    question: Optional[str] = None


# Palm Reading Schemas
class PalmReadingCreate(BaseModel):
    """Schema for creating a palm reading"""
    hand_image_url: HttpUrl
    hand_type: str = Field(..., regex="^(left|right)$")


# Generic Reading Response
class SymbolDetected(BaseModel):
    """Detected symbol in reading"""
    symbol: str
    position: Optional[str] = None
    clarity: Optional[int] = Field(None, ge=1, le=10)
    meaning: Optional[str] = None


class ReadingImageResponse(BaseModel):
    """Reading image details"""
    id: int
    image_url: str
    image_type: Optional[str] = None
    annotated_url: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True


class ReadingResponse(BaseModel):
    """Schema for reading in API responses"""
    id: int
    user_id: int
    type: ReadingType
    input_data: Dict[str, Any]
    ai_response: str
    symbols_detected: Optional[List[Dict[str, Any]]] = None
    rating: Optional[int] = None
    feedback_text: Optional[str] = None
    processing_time_ms: Optional[int] = None
    created_at: datetime
    images: List[ReadingImageResponse] = []

    class Config:
        from_attributes = True


# Reading feedback
class ReadingFeedback(BaseModel):
    """Schema for submitting reading feedback"""
    rating: int = Field(..., ge=1, le=5)
    feedback_text: Optional[str] = Field(None, max_length=1000)


# Reading list response
class ReadingListResponse(BaseModel):
    """Schema for paginated reading list"""
    readings: List[ReadingResponse]
    total: int
    has_more: bool
