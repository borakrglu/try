"""
Chat API endpoints - Persona-based conversations
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.chat import PersonaType
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatHistoryResponse
)
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def send_chat_message(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to an AI persona and receive a response

    **Personas:**
    - **sage**: Stoic philosopher offering wisdom and reflection
    - **witch**: Earthy mystic with crystal, herb, and moon magic
    - **astrologer**: Cosmic guide focused on planetary transits

    **Request Body:**
    - **persona**: Which AI persona to talk to (sage/witch/astrologer)
    - **message**: Your message (1-2000 characters)
    - **related_reading_id**: Optional - reference a specific reading

    **Features:**
    - Remembers your past readings and conversations
    - Provides personalized guidance based on your zodiac sign
    - Context-aware responses that reference your journey
    - Long-term memory across conversations

    **Returns:**
    The AI persona's response with metadata (response time, token usage)

    **Example:**
    ```json
    {
      "persona": "sage",
      "message": "I'm feeling anxious about a big decision I need to make.",
      "related_reading_id": null
    }
    ```
    """

    chat_service = ChatService(db)

    try:
        # Send message and get response
        user_message, assistant_message = await chat_service.send_message(
            user=current_user,
            message_data=message_data
        )

        # Return assistant's response
        return ChatMessageResponse.model_validate(assistant_message)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    persona: Optional[PersonaType] = Query(None, description="Filter by persona"),
    limit: int = Query(50, ge=1, le=100, description="Number of messages to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get your chat conversation history

    **Query Parameters:**
    - **persona**: Filter by specific persona (sage/witch/astrologer). Leave empty for all conversations.
    - **limit**: Number of messages to return (1-100, default: 50)
    - **offset**: Skip this many messages for pagination (default: 0)

    **Returns:**
    List of messages with pagination info

    **Example Response:**
    ```json
    {
      "messages": [
        {
          "id": 1,
          "user_id": 123,
          "persona": "sage",
          "role": "user",
          "content": "How do I find peace?",
          "created_at": "2026-01-12T10:00:00Z"
        },
        {
          "id": 2,
          "user_id": 123,
          "persona": "sage",
          "role": "assistant",
          "content": "Peace begins with accepting...",
          "response_time_ms": 2500,
          "created_at": "2026-01-12T10:00:03Z"
        }
      ],
      "total": 42,
      "has_more": false
    }
    ```
    """

    chat_service = ChatService(db)

    try:
        history = await chat_service.get_conversation_history(
            user=current_user,
            persona=persona,
            limit=limit,
            offset=offset
        )

        return history

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chat history: {str(e)}"
        )


@router.delete("/history", status_code=status.HTTP_200_OK)
async def delete_chat_history(
    persona: Optional[PersonaType] = Query(None, description="Delete only this persona's messages"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete your chat conversation history

    **Warning:** This action cannot be undone!

    **Query Parameters:**
    - **persona**: Delete only messages with this persona (sage/witch/astrologer).
                  Leave empty to delete ALL conversations.

    **Returns:**
    Number of messages deleted

    **Example Response:**
    ```json
    {
      "message": "Successfully deleted 42 messages",
      "count": 42
    }
    ```
    """

    chat_service = ChatService(db)

    try:
        count = await chat_service.delete_conversation(
            user=current_user,
            persona=persona
        )

        persona_text = f" with {persona.value}" if persona else ""
        return {
            "message": f"Successfully deleted {count} messages{persona_text}",
            "count": count
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete chat history: {str(e)}"
        )


@router.get("/memory-stats", status_code=status.HTTP_200_OK)
async def get_memory_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics about your chat memory

    Shows how many conversations you've had with each persona
    and information about your vector memory (long-term context storage).

    **Returns:**
    Memory statistics and usage info

    **Example Response:**
    ```json
    {
      "total_messages": 156,
      "by_persona": {
        "sage": 42,
        "witch": 68,
        "astrologer": 46
      },
      "vector_memory": {
        "enabled": true,
        "vector_count": 156,
        "index_fullness": 0.002
      }
    }
    ```
    """

    chat_service = ChatService(db)

    try:
        stats = await chat_service.get_memory_stats(current_user)
        return stats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve memory stats: {str(e)}"
        )


@router.get("/personas", status_code=status.HTTP_200_OK)
def get_available_personas():
    """
    Get information about available AI personas

    Returns details about each persona's personality, expertise, and communication style.

    **Returns:**
    List of personas with descriptions

    **Example Response:**
    ```json
    {
      "personas": [
        {
          "id": "sage",
          "name": "The Sage",
          "description": "A wise stoic philosopher...",
          "expertise": ["philosophy", "mindfulness", "meditation"],
          "tone": "Calm, thoughtful, Socratic"
        },
        ...
      ]
    }
    ```
    """

    personas = [
        {
            "id": "sage",
            "name": "The Sage",
            "description": "A wise stoic philosopher and spiritual guide who helps you find inner peace through reflective questions and mindfulness practices.",
            "expertise": [
                "Stoic philosophy (Marcus Aurelius, Epictetus, Seneca)",
                "Buddhist mindfulness and compassion",
                "Taoist wisdom about flow and balance",
                "Meditation and journaling practices",
                "Turning obstacles into opportunities"
            ],
            "tone": "Calm, thoughtful, Socratic, patient",
            "best_for": [
                "Finding clarity in difficult situations",
                "Developing inner strength and resilience",
                "Philosophical questions about life and meaning",
                "Meditation and mindfulness guidance",
                "Managing anxiety and stress through wisdom"
            ],
            "example_response": "Anxiety often rehearses a future that hasn't happened. What if you viewed tomorrow as simply another conversation, not a test of your worth? As Marcus Aurelius said: 'You have power over your mind—not outside events.'"
        },
        {
            "id": "witch",
            "name": "The Witch",
            "description": "An earthy, practical mystic who offers tangible magical tools like crystals, herbs, and moon rituals to help you connect with natural energies.",
            "expertise": [
                "Crystal properties and healing",
                "Herbal remedies and natural magic",
                "Moon phases and lunar magic",
                "Simple rituals and spellwork",
                "Connecting with natural cycles",
                "Chakra balancing"
            ],
            "tone": "Warm, grounded, mystical, playful",
            "best_for": [
                "Practical magic and daily rituals",
                "Crystal and herb recommendations",
                "Moon phase guidance",
                "Grounding and energy work",
                "Natural remedies for common challenges",
                "Manifesting intentions"
            ],
            "example_response": "Ah, confidence needs tending. Carry Citrine—the 'success stone.' It amplifies personal power. Each morning, hold it and say: 'I am capable, I am worthy.' The New Moon in 3 days is perfect for intentions. 🔥"
        },
        {
            "id": "astrologer",
            "name": "The Astrologer",
            "description": "A cosmic guide and expert in planetary movements who helps you understand celestial influences and optimal timing for your actions.",
            "expertise": [
                "Natal chart interpretation",
                "Planetary transits and aspects",
                "Moon phases and their meanings",
                "Mercury retrograde guidance",
                "Zodiac sign traits and compatibility",
                "Timing advice for important decisions",
                "House systems and life areas"
            ],
            "tone": "Cosmic yet grounded, analytical, inspiring",
            "best_for": [
                "Understanding how current planetary movements affect you",
                "Timing guidance (when to act, when to wait)",
                "Zodiac sign insights and compatibility",
                "Navigating Mercury retrograde",
                "Career and relationship timing",
                "Connecting cosmic events to daily life"
            ],
            "example_response": "As a Leo, Mars is transiting your 10th house of career—your cosmic green light! The Waxing Moon supports initiation. But finalize by Jan 20 before Mercury's shadow. The stars align for your ambition. ✨"
        }
    ]

    return {"personas": personas}
