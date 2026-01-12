"""
Reading API endpoints - Coffee, Tarot, Palm readings
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.user import User
from app.models.reading import ReadingType
from app.schemas.reading import (
    CoffeeReadingCreate,
    TarotReadingCreate,
    ReadingResponse,
    ReadingListResponse,
    ReadingFeedback
)
from app.services.reading_service import ReadingService
from app.api.deps import get_current_user, check_reading_limit

router = APIRouter()


@router.post("/coffee", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
async def create_coffee_reading(
    reading_data: CoffeeReadingCreate,
    current_user: User = Depends(check_reading_limit),
    db: Session = Depends(get_db)
):
    """
    Create a coffee cup reading

    **Requires:** Premium or free tier with readings available (3/month)

    **Process:**
    1. Upload 3 images of your coffee cup (separate endpoint or base64)
    2. AI analyzes images for symbols using Vision API
    3. AI generates personalized reading based on symbols + your zodiac
    4. Reading is saved to your library

    **Returns:** Complete coffee fortune reading with detected symbols

    **Time:** ~10-15 seconds

    **Example:**
    ```json
    {
      "cup_image_url": "https://...",
      "saucer_image_url": "https://...",
      "side_image_url": "https://..."
    }
    ```
    """
    reading_service = ReadingService(db)

    # Collect image URLs
    image_urls = [
        str(reading_data.cup_image_url),
        str(reading_data.saucer_image_url),
        str(reading_data.side_image_url)
    ]

    # Create reading (async processing)
    reading = await reading_service.create_coffee_reading(
        user=current_user,
        image_urls=image_urls
    )

    return ReadingResponse.from_orm(reading)


@router.post("/tarot", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
async def create_tarot_reading(
    reading_data: TarotReadingCreate,
    current_user: User = Depends(check_reading_limit),
    db: Session = Depends(get_db)
):
    """
    Create a tarot card reading

    **Requires:** Premium or free tier with readings available (3/month)

    **Process:**
    1. Choose your spread type (single card, three card, Celtic Cross, etc.)
    2. Optionally provide a question or focus area
    3. AI draws random cards and generates personalized reading
    4. Reading is saved to your library

    **Spread Types:**
    - `single_card`: Quick daily guidance (1 card)
    - `three_card`: Past-Present-Future spread (3 cards)
    - `celtic_cross`: Comprehensive 10-card spread
    - `horseshoe`: Balanced 7-card guidance
    - `relationship`: 7-card relationship insight
    - `career`: 5-card career guidance

    **Returns:** Complete tarot reading with drawn cards and interpretation

    **Time:** ~10-15 seconds

    **Example:**
    ```json
    {
      "spread_type": "three_card",
      "question": "What should I focus on this week?"
    }
    ```
    """
    reading_service = ReadingService(db)

    # Create tarot reading (cards drawn automatically)
    reading = await reading_service.create_tarot_reading(
        user=current_user,
        spread_type=reading_data.spread_type,
        question=reading_data.question
    )

    return ReadingResponse.from_orm(reading)


@router.get("/{reading_id}", response_model=ReadingResponse)
def get_reading(
    reading_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific reading by ID

    **Requires:** Authentication

    Only returns readings that belong to the authenticated user
    """
    reading_service = ReadingService(db)
    reading = reading_service.get_reading_by_id(reading_id, current_user)

    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading not found"
        )

    return ReadingResponse.from_orm(reading)


@router.get("", response_model=ReadingListResponse)
def list_readings(
    type: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List user's readings with pagination

    **Query Parameters:**
    - `type`: Filter by reading type (coffee, tarot, palm)
    - `limit`: Number of readings to return (default: 10, max: 50)
    - `offset`: Pagination offset (default: 0)

    **Returns:** Paginated list of readings
    """
    # Validate limit
    if limit > 50:
        limit = 50

    # Parse reading type
    reading_type = None
    if type:
        try:
            reading_type = ReadingType(type.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid reading type. Must be: coffee, tarot, or palm"
            )

    reading_service = ReadingService(db)
    readings, total = reading_service.get_user_readings(
        user=current_user,
        reading_type=reading_type,
        limit=limit,
        offset=offset
    )

    return ReadingListResponse(
        readings=[ReadingResponse.from_orm(r) for r in readings],
        total=total,
        has_more=(offset + limit) < total
    )


@router.post("/{reading_id}/feedback", response_model=ReadingResponse)
def submit_reading_feedback(
    reading_id: int,
    feedback: ReadingFeedback,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a reading

    **Body:**
    - `rating`: 1-5 stars
    - `feedback_text`: Optional text feedback

    **Returns:** Updated reading
    """
    reading_service = ReadingService(db)

    try:
        reading = reading_service.rate_reading(
            reading_id=reading_id,
            user=current_user,
            rating=feedback.rating,
            feedback=feedback.feedback_text
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    return ReadingResponse.from_orm(reading)


# TODO: Add tarot and palm reading endpoints
# @router.post("/tarot", response_model=ReadingResponse)
# async def create_tarot_reading(...)
#
# @router.post("/palm", response_model=ReadingResponse)
# async def create_palm_reading(...)
