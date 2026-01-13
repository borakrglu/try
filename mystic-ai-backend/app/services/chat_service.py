"""
Chat Service - Manage persona-based conversations with long-term memory
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import time
import logging

from openai import AsyncOpenAI

from app.models.chat import ChatMessage, PersonaType, MessageRole
from app.models.user import User
from app.models.reading import Reading, ReadingType
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse, ChatHistoryResponse
from app.config import settings
from app.ai.prompts.chat_personas import get_persona_prompt, get_system_context
from app.services.vector_memory import VectorMemoryService

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service for managing AI chat conversations with personas

    Features:
    - 3 distinct personas (Sage, Witch, Astrologer)
    - Long-term memory via Pinecone vector database
    - Context-aware responses based on user history
    - Conversation history management
    """

    def __init__(self, db: Session):
        """
        Initialize chat service

        Args:
            db: Database session
        """
        self.db = db
        self.ai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.vector_memory = VectorMemoryService()

    async def send_message(
        self,
        user: User,
        message_data: ChatMessageCreate
    ) -> tuple[ChatMessage, ChatMessage]:
        """
        Process user message and generate AI response

        Args:
            user: User object
            message_data: Message content and persona

        Returns:
            Tuple of (user_message, assistant_message)
        """
        start_time = time.time()

        # Store user message
        user_message = ChatMessage(
            user_id=user.id,
            persona=message_data.persona,
            role=MessageRole.USER,
            content=message_data.message,
            related_reading_id=message_data.related_reading_id
        )
        self.db.add(user_message)
        self.db.commit()
        self.db.refresh(user_message)

        logger.info(f"User {user.id} sent message to {message_data.persona}: {message_data.message[:50]}...")

        # Store in vector memory (async, non-blocking)
        if self.vector_memory.is_enabled():
            await self.vector_memory.store_message(
                user_id=user.id,
                message_id=user_message.id,
                content=message_data.message,
                persona=message_data.persona.value,
                role=MessageRole.USER.value
            )

        # Get conversation context
        context = await self._build_context(
            user=user,
            persona=message_data.persona,
            current_message=message_data.message
        )

        # Generate AI response
        ai_response, response_time_ms = await self._generate_response(
            user=user,
            persona=message_data.persona,
            conversation_history=context["conversation_history"],
            system_context=context["system_context"],
            current_message=message_data.message
        )

        # Store assistant message
        assistant_message = ChatMessage(
            user_id=user.id,
            persona=message_data.persona,
            role=MessageRole.ASSISTANT,
            content=ai_response,
            related_reading_id=message_data.related_reading_id,
            response_time_ms=response_time_ms
        )
        self.db.add(assistant_message)
        self.db.commit()
        self.db.refresh(assistant_message)

        # Store assistant response in vector memory
        if self.vector_memory.is_enabled():
            await self.vector_memory.store_message(
                user_id=user.id,
                message_id=assistant_message.id,
                content=ai_response,
                persona=message_data.persona.value,
                role=MessageRole.ASSISTANT.value
            )

        total_time = int((time.time() - start_time) * 1000)
        logger.info(f"Chat response generated in {total_time}ms (AI: {response_time_ms}ms)")

        return user_message, assistant_message

    async def _build_context(
        self,
        user: User,
        persona: PersonaType,
        current_message: str
    ) -> Dict[str, Any]:
        """
        Build context for AI response

        Args:
            user: User object
            persona: Selected persona
            current_message: Current user message

        Returns:
            Dictionary with conversation_history and system_context
        """

        # Get recent conversation history (last 10 messages with this persona)
        recent_messages = (
            self.db.query(ChatMessage)
            .filter(
                ChatMessage.user_id == user.id,
                ChatMessage.persona == persona
            )
            .order_by(ChatMessage.created_at.desc())
            .limit(10)
            .all()
        )
        recent_messages.reverse()  # Oldest first

        conversation_history = [
            {
                "role": msg.role.value,
                "content": msg.content
            }
            for msg in recent_messages
        ]

        # Get recent readings summary
        recent_readings = await self._get_recent_readings_summary(user)

        # Build system context
        system_context = get_system_context(
            user_data={
                "name": user.name,
                "zodiac": user.zodiac_sign or "Unknown",
                "language": user.language.value
            },
            recent_readings=recent_readings,
            conversation_history=conversation_history
        )

        # Optionally retrieve relevant past context from vector memory
        if self.vector_memory.is_enabled():
            relevant_context = await self.vector_memory.retrieve_context(
                user_id=user.id,
                query=current_message,
                persona=persona.value,
                top_k=3
            )

            if relevant_context:
                # Add relevant past conversations to system context
                relevant_snippets = [
                    f"[Past conversation] {ctx['content'][:200]}..."
                    for ctx in relevant_context
                    if ctx['score'] > 0.7  # Only high-relevance matches
                ]
                if relevant_snippets:
                    system_context += "\n\n**RELEVANT PAST CONTEXT:**\n" + "\n".join(relevant_snippets)

        return {
            "conversation_history": conversation_history,
            "system_context": system_context
        }

    async def _get_recent_readings_summary(self, user: User) -> List[Dict[str, Any]]:
        """
        Get summary of user's recent readings

        Args:
            user: User object

        Returns:
            List of reading summaries
        """
        recent_readings = (
            self.db.query(Reading)
            .filter(Reading.user_id == user.id)
            .order_by(Reading.created_at.desc())
            .limit(3)
            .all()
        )

        summaries = []
        for reading in recent_readings:
            # Extract first 150 chars as summary
            content_preview = reading.content[:150] + "..." if len(reading.content) > 150 else reading.content

            summaries.append({
                "type": reading.reading_type.value,
                "summary": content_preview,
                "date": reading.created_at.strftime("%Y-%m-%d")
            })

        return summaries

    async def _generate_response(
        self,
        user: User,
        persona: PersonaType,
        conversation_history: List[Dict[str, str]],
        system_context: str,
        current_message: str
    ) -> tuple[str, int]:
        """
        Generate AI response using OpenAI

        Args:
            user: User object
            persona: Selected persona
            conversation_history: Recent conversation messages
            system_context: System context string
            current_message: Current user message

        Returns:
            Tuple of (response_text, processing_time_ms)
        """
        start_time = time.time()

        # Get recent readings for context
        recent_readings_summary = "No recent readings"
        recent_readings = await self._get_recent_readings_summary(user)
        if recent_readings:
            recent_readings_summary = "; ".join([
                f"{r['type']} on {r['date']}: {r['summary']}"
                for r in recent_readings
            ])

        # Build persona system prompt
        system_prompt = get_persona_prompt(
            persona_type=persona.value,
            user_name=user.name,
            zodiac_sign=user.zodiac_sign or "Unknown",
            recent_reading_summary=recent_readings_summary,
            language=user.language.value,
            moon_phase=self._get_current_moon_phase(),  # TODO: Implement real moon phase
            current_transits=self._get_current_transits() if persona == PersonaType.ASTROLOGER else "",
            user_context=system_context
        )

        # Build messages for API
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add conversation history (last 5 exchanges to stay within context)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": current_message
        })

        logger.info(f"Generating {persona.value} response with {len(messages)} messages in context")

        try:
            response = await self.ai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.8,  # Conversational and warm
                max_tokens=500,  # ~150-200 words
            )

            response_text = response.choices[0].message.content
            processing_time = int((time.time() - start_time) * 1000)

            return response_text, processing_time

        except Exception as e:
            logger.error(f"OpenAI API error in chat: {str(e)}")
            # Fallback response
            fallback = self._get_fallback_response(persona, user.name)
            processing_time = int((time.time() - start_time) * 1000)
            return fallback, processing_time

    def _get_current_moon_phase(self) -> str:
        """
        Get current moon phase

        TODO: Integrate with real moon phase API
        For now, returns a placeholder
        """
        return "Waxing Crescent"

    def _get_current_transits(self) -> str:
        """
        Get current astrological transits

        TODO: Integrate with astrology API
        For now, returns a placeholder
        """
        now = datetime.utcnow()
        return f"Moon in transition (as of {now.strftime('%B %d')}), Mercury direct, Venus harmonious"

    def _get_fallback_response(self, persona: PersonaType, user_name: str) -> str:
        """
        Get fallback response if API fails

        Args:
            persona: Persona type
            user_name: User's name

        Returns:
            Fallback message
        """
        fallbacks = {
            PersonaType.SAGE: f"{user_name}, I sense a moment of silence in our connection. Sometimes the wisest response is to pause, reflect, and return when clarity emerges. I'm here when you're ready.",

            PersonaType.WITCH: f"{user_name}, the cosmic energies are swirling at the moment. Even a witch needs to recharge! Try lighting a candle, taking three deep breaths, and we'll reconnect shortly. 🕯️",

            PersonaType.ASTROLOGER: f"{user_name}, the stars are momentarily obscured by cosmic clouds. In astrology, we call these 'void of course' moments—a time to pause before proceeding. I'll be back shortly! ✨"
        }

        return fallbacks.get(persona, "I'm experiencing a moment of cosmic turbulence. Let's try again in a moment.")

    async def get_conversation_history(
        self,
        user: User,
        persona: Optional[PersonaType] = None,
        limit: int = 50,
        offset: int = 0
    ) -> ChatHistoryResponse:
        """
        Get user's chat history

        Args:
            user: User object
            persona: Filter by persona (optional)
            limit: Number of messages to return
            offset: Pagination offset

        Returns:
            Chat history response
        """

        query = self.db.query(ChatMessage).filter(ChatMessage.user_id == user.id)

        if persona:
            query = query.filter(ChatMessage.persona == persona)

        # Get total count
        total = query.count()

        # Get paginated messages
        messages = (
            query
            .order_by(ChatMessage.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        messages.reverse()  # Return oldest first

        return ChatHistoryResponse(
            messages=[ChatMessageResponse.model_validate(msg) for msg in messages],
            total=total,
            has_more=(offset + limit) < total
        )

    async def delete_conversation(
        self,
        user: User,
        persona: Optional[PersonaType] = None
    ) -> int:
        """
        Delete conversation history

        Args:
            user: User object
            persona: Delete only this persona's messages (optional)

        Returns:
            Number of messages deleted
        """

        query = self.db.query(ChatMessage).filter(ChatMessage.user_id == user.id)

        if persona:
            query = query.filter(ChatMessage.persona == persona)

        count = query.count()
        query.delete()
        self.db.commit()

        # Also delete from vector memory
        if self.vector_memory.is_enabled() and not persona:
            # Only delete all if no specific persona
            await self.vector_memory.delete_user_memory(user.id)

        logger.info(f"Deleted {count} messages for user {user.id}")

        return count

    async def get_memory_stats(self, user: User) -> Dict[str, Any]:
        """
        Get statistics about user's chat memory

        Args:
            user: User object

        Returns:
            Memory statistics
        """

        # Database stats
        total_messages = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.user_id == user.id)
            .count()
        )

        by_persona = {}
        for persona in PersonaType:
            count = (
                self.db.query(ChatMessage)
                .filter(
                    ChatMessage.user_id == user.id,
                    ChatMessage.persona == persona
                )
                .count()
            )
            by_persona[persona.value] = count

        # Vector memory stats
        vector_stats = await self.vector_memory.get_memory_stats(user.id)

        return {
            "total_messages": total_messages,
            "by_persona": by_persona,
            "vector_memory": vector_stats
        }
