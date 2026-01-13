"""
Journal API endpoints - Daily journaling with AI-powered insights
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.journal import (
    JournalEntryCreate,
    JournalEntryUpdate,
    JournalEntryResponse,
    JournalInsightsResponse,
    MoodCalendarResponse
)
from app.services.journal_service import JournalService

router = APIRouter()


@router.post("/entries", response_model=JournalEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_journal_entry(
    entry_data: JournalEntryCreate,
    analyze: bool = Query(True, description="Perform AI sentiment and chakra analysis"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new journal entry with optional AI analysis

    **Entry Types:**
    - **journal**: Daily journal entry (default)
    - **dream**: Dream journal with symbol interpretation
    - **gratitude**: Gratitude list (no AI analysis)

    **Request Body:**
    - **content**: Journal entry text (1-10000 characters)
    - **entry_type**: Type of entry (journal/dream/gratitude)
    - **mood**: Optional mood indicator (emoji or text)
    - **tags**: Optional tags for categorization (work, love, family, etc.)

    **AI Analysis (when enabled):**
    - Sentiment detection (joy, sadness, anxiety, calm, etc.)
    - Energy level scoring (1-10)
    - Stress indicators identification
    - 7 Chakra energy scoring:
      * Root (security, stability)
      * Sacral (creativity, pleasure)
      * Solar Plexus (confidence, power)
      * Heart (love, compassion)
      * Throat (communication, expression)
      * Third Eye (intuition, insight)
      * Crown (spirituality, purpose)
    - Personalized affirmation generation

    **Gamification:**
    - Earn +10 karma points per entry
    - Earn +50 bonus karma for 7-day streaks
    - Track journal streaks automatically

    **Returns:**
    Journal entry with complete AI analysis and affirmation

    **Example:**
    ```json
    {
      "content": "Today was challenging. I had a difficult conversation with my boss about project delays. Feeling anxious but also relieved that I spoke up.",
      "entry_type": "journal",
      "mood": "anxious",
      "tags": ["work", "communication"]
    }
    ```
    """

    journal_service = JournalService(db)

    try:
        entry = await journal_service.create_entry(
            user=current_user,
            entry_data=entry_data,
            analyze=analyze
        )

        return JournalEntryResponse.model_validate(entry)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create journal entry: {str(e)}"
        )


@router.get("/entries", response_model=List[JournalEntryResponse])
async def list_journal_entries(
    entry_type: Optional[str] = Query(None, regex="^(journal|dream|gratitude)$", description="Filter by entry type"),
    limit: int = Query(50, ge=1, le=100, description="Number of entries to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get your journal entries

    **Query Parameters:**
    - **entry_type**: Filter by type (journal/dream/gratitude). Leave empty for all entries.
    - **limit**: Number of entries to return (1-100, default: 50)
    - **offset**: Skip this many entries for pagination (default: 0)

    **Returns:**
    List of journal entries, sorted by most recent first

    **Example Response:**
    ```json
    [
      {
        "id": 123,
        "user_id": 456,
        "content": "Today was amazing...",
        "entry_type": "journal",
        "mood": "joyful",
        "tags": ["gratitude", "family"],
        "sentiment_analysis": {
          "primary_emotion": "joy",
          "energy_level": 8,
          "summary": "Feeling grateful and energized"
        },
        "chakra_scores": {
          "root": 8,
          "sacral": 7,
          "solar_plexus": 8,
          "heart": 9,
          "throat": 7,
          "third_eye": 6,
          "crown": 7
        },
        "generated_affirmation": "I embrace joy and share my light with those I love.",
        "created_at": "2026-01-12T10:00:00Z",
        "updated_at": "2026-01-12T10:00:00Z"
      }
    ]
    ```
    """

    journal_service = JournalService(db)

    try:
        entries = await journal_service.get_entries(
            user=current_user,
            entry_type=entry_type,
            limit=limit,
            offset=offset
        )

        return [JournalEntryResponse.model_validate(entry) for entry in entries]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve journal entries: {str(e)}"
        )


@router.get("/entries/{entry_id}", response_model=JournalEntryResponse)
async def get_journal_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific journal entry by ID

    **Path Parameters:**
    - **entry_id**: Journal entry ID

    **Returns:**
    Journal entry with full analysis

    **Errors:**
    - 404: Entry not found or doesn't belong to you
    """

    journal_service = JournalService(db)

    entry = await journal_service.get_entry_by_id(current_user, entry_id)

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )

    return JournalEntryResponse.model_validate(entry)


@router.put("/entries/{entry_id}", response_model=JournalEntryResponse)
async def update_journal_entry(
    entry_id: int,
    update_data: JournalEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a journal entry

    **Note:** Updating content does NOT re-run AI analysis. AI analysis is only performed on creation.

    **Path Parameters:**
    - **entry_id**: Journal entry ID

    **Request Body:**
    - **content**: Updated entry text (optional)
    - **mood**: Updated mood (optional)
    - **tags**: Updated tags (optional)

    **Returns:**
    Updated journal entry

    **Errors:**
    - 404: Entry not found or doesn't belong to you
    """

    journal_service = JournalService(db)

    entry = await journal_service.update_entry(
        user=current_user,
        entry_id=entry_id,
        update_data=update_data
    )

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )

    return JournalEntryResponse.model_validate(entry)


@router.delete("/entries/{entry_id}", status_code=status.HTTP_200_OK)
async def delete_journal_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a journal entry

    **Warning:** This action cannot be undone!

    **Path Parameters:**
    - **entry_id**: Journal entry ID

    **Returns:**
    Confirmation message

    **Errors:**
    - 404: Entry not found or doesn't belong to you
    """

    journal_service = JournalService(db)

    deleted = await journal_service.delete_entry(current_user, entry_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found"
        )

    return {
        "message": "Journal entry deleted successfully",
        "entry_id": entry_id
    }


@router.get("/insights", status_code=status.HTTP_200_OK)
async def get_journal_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive journal insights

    Analyzes your recent journal entries (last 7 days) to provide:
    - **Chakra Balance**: Average scores across all 7 chakras
    - **Mood Insights**: Energy level, dominant emotion, mood trend
    - **Journal Streak**: Current and longest journal streaks
    - **Affirmation of the Day**: Personalized affirmation

    **Mood Trends:**
    - **improving**: Energy and mood increasing over time
    - **declining**: Concerning downward trend (consider self-care)
    - **stable**: Consistent emotional state
    - **fluctuating**: Variable moods (common during transitions)

    **Returns:**
    Complete insights package

    **Example Response:**
    ```json
    {
      "chakra_balance": {
        "root": 7,
        "sacral": 6,
        "solar_plexus": 5,
        "heart": 8,
        "throat": 6,
        "third_eye": 7,
        "crown": 6
      },
      "mood_insights": {
        "current_mood": "calm",
        "energy_level": 7,
        "stress_level": 3,
        "dominant_emotion": "contentment",
        "mood_trend": "improving"
      },
      "journal_streak": 12,
      "total_entries": 47,
      "affirmation_of_the_day": "I am grounded in my truth and open to life's flow."
    }
    ```
    """

    journal_service = JournalService(db)

    try:
        insights = await journal_service.get_insights(current_user)
        return insights

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate insights: {str(e)}"
        )


@router.get("/calendar/{year}/{month}", response_model=MoodCalendarResponse)
async def get_mood_calendar(
    year: int = Query(..., ge=2020, le=2030, description="Year"),
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get mood calendar for a specific month

    Provides a day-by-day view of your journal entries, moods, and energy levels.

    **Path Parameters:**
    - **year**: Year (2020-2030)
    - **month**: Month (1-12)

    **Returns:**
    Calendar with daily mood/energy data

    **Use Cases:**
    - Visualize mood patterns over time
    - Identify specific stressful periods
    - Track consistency of journaling practice
    - See energy level fluctuations

    **Example Response:**
    ```json
    {
      "year": 2026,
      "month": 1,
      "days": [
        {
          "date": "2026-01-01T00:00:00Z",
          "mood": "hopeful",
          "energy_level": 7,
          "has_entry": true
        },
        {
          "date": "2026-01-02T00:00:00Z",
          "mood": null,
          "energy_level": null,
          "has_entry": false
        }
      ]
    }
    ```
    """

    journal_service = JournalService(db)

    try:
        calendar = await journal_service.get_mood_calendar(
            user=current_user,
            year=year,
            month=month
        )

        return calendar

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate mood calendar: {str(e)}"
        )


@router.get("/stats", status_code=status.HTTP_200_OK)
async def get_journal_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get journal statistics

    **Returns:**
    Statistics about your journaling practice

    **Metrics:**
    - Total entries (all types)
    - Entries by type (journal/dream/gratitude)
    - Current streak
    - Longest streak
    - Average entries per week
    - Last entry date

    **Example Response:**
    ```json
    {
      "total_entries": 47,
      "by_type": {
        "journal": 32,
        "dream": 10,
        "gratitude": 5
      },
      "current_streak": 12,
      "longest_streak": 18,
      "avg_per_week": 4.2,
      "last_entry_date": "2026-01-12T10:00:00Z"
    }
    ```
    """

    journal_service = JournalService(db)

    try:
        all_entries = await journal_service.get_entries(
            user=current_user,
            limit=1000  # Get all for stats
        )

        # Count by type
        by_type = {"journal": 0, "dream": 0, "gratitude": 0}
        for entry in all_entries:
            by_type[entry.entry_type] = by_type.get(entry.entry_type, 0) + 1

        # Get streak from user stats
        from app.models.user_stats import UserStats
        stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()

        return {
            "total_entries": len(all_entries),
            "by_type": by_type,
            "current_streak": stats.current_journal_streak if stats else 0,
            "longest_streak": stats.longest_journal_streak if stats else 0,
            "avg_per_week": round(len(all_entries) / 52, 1) if len(all_entries) > 0 else 0,
            "last_entry_date": all_entries[0].created_at if all_entries else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate stats: {str(e)}"
        )
