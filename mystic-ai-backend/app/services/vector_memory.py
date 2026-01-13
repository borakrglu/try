"""
Vector Memory Service - Pinecone integration for long-term chat memory

This service manages semantic memory for chat conversations, allowing personas
to remember and retrieve relevant context from past interactions.
"""

from typing import List, Dict, Any, Optional
import hashlib
from datetime import datetime

try:
    from pinecone import Pinecone, ServerlessSpec
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("Warning: Pinecone not installed. Vector memory will be disabled.")

from app.config import settings


class VectorMemoryService:
    """
    Service for storing and retrieving conversation context using Pinecone vector database

    This enables long-term memory for AI personas by:
    - Storing conversation turns with embeddings
    - Retrieving relevant past context based on current query
    - Maintaining separate namespaces per user
    """

    def __init__(self):
        """Initialize Pinecone connection"""
        self.enabled = False
        self.index = None
        self.pc = None

        if not PINECONE_AVAILABLE:
            print("Pinecone SDK not available. Vector memory disabled.")
            return

        if not settings.PINECONE_API_KEY:
            print("PINECONE_API_KEY not configured. Vector memory disabled.")
            return

        try:
            # Initialize Pinecone client
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)

            # Check if index exists, create if not
            index_name = settings.PINECONE_INDEX_NAME

            existing_indexes = self.pc.list_indexes()
            index_names = [idx.name for idx in existing_indexes]

            if index_name not in index_names:
                print(f"Creating Pinecone index: {index_name}")
                self.pc.create_index(
                    name=index_name,
                    dimension=1536,  # OpenAI text-embedding-ada-002 dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )

            # Connect to index
            self.index = self.pc.Index(index_name)
            self.enabled = True
            print(f"Pinecone vector memory initialized: {index_name}")

        except Exception as e:
            print(f"Failed to initialize Pinecone: {e}")
            self.enabled = False

    def is_enabled(self) -> bool:
        """Check if vector memory is available"""
        return self.enabled and self.index is not None

    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        # This would use OpenAI's embedding API
        # For now, returning a placeholder
        # TODO: Integrate with OpenAI embedding API
        import random
        return [random.random() for _ in range(1536)]

    def _generate_id(self, user_id: int, message_id: int) -> str:
        """
        Generate unique ID for vector

        Args:
            user_id: User ID
            message_id: Message ID

        Returns:
            Unique vector ID
        """
        return f"user_{user_id}_msg_{message_id}"

    async def store_message(
        self,
        user_id: int,
        message_id: int,
        content: str,
        persona: str,
        role: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store a message in vector memory

        Args:
            user_id: User ID
            message_id: Chat message ID
            content: Message content
            persona: Persona type (sage/witch/astrologer)
            role: Message role (user/assistant)
            metadata: Additional metadata

        Returns:
            Success status
        """
        if not self.is_enabled():
            return False

        try:
            # Generate embedding
            embedding = self._generate_embedding(content)

            # Prepare metadata
            vector_metadata = {
                "user_id": user_id,
                "message_id": message_id,
                "content": content[:1000],  # Truncate for metadata storage
                "persona": persona,
                "role": role,
                "timestamp": datetime.utcnow().isoformat(),
                **(metadata or {})
            }

            # Store in Pinecone
            vector_id = self._generate_id(user_id, message_id)
            self.index.upsert(
                vectors=[(vector_id, embedding, vector_metadata)],
                namespace=f"user_{user_id}"
            )

            return True

        except Exception as e:
            print(f"Error storing message in vector memory: {e}")
            return False

    async def retrieve_context(
        self,
        user_id: int,
        query: str,
        persona: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant past context for a query

        Args:
            user_id: User ID
            query: Current user query
            persona: Filter by persona (optional)
            top_k: Number of results to return

        Returns:
            List of relevant past messages with metadata
        """
        if not self.is_enabled():
            return []

        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query)

            # Build filter
            filter_dict = {}
            if persona:
                filter_dict["persona"] = persona

            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                namespace=f"user_{user_id}",
                filter=filter_dict if filter_dict else None,
                include_metadata=True
            )

            # Extract matches
            context = []
            for match in results.matches:
                context.append({
                    "score": match.score,
                    "content": match.metadata.get("content", ""),
                    "role": match.metadata.get("role", ""),
                    "persona": match.metadata.get("persona", ""),
                    "timestamp": match.metadata.get("timestamp", ""),
                    "metadata": match.metadata
                })

            return context

        except Exception as e:
            print(f"Error retrieving context from vector memory: {e}")
            return []

    async def get_recent_conversation(
        self,
        user_id: int,
        persona: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent conversation history (fallback when vector search not needed)

        This is a simplified version that would query the database directly
        for recent messages. In practice, this should query the ChatMessage model.

        Args:
            user_id: User ID
            persona: Persona type
            limit: Number of recent messages

        Returns:
            Recent messages
        """
        # This should query the database directly
        # For now, returning empty list as this is handled by ChatService
        return []

    async def delete_user_memory(self, user_id: int) -> bool:
        """
        Delete all vector memory for a user

        Args:
            user_id: User ID

        Returns:
            Success status
        """
        if not self.is_enabled():
            return False

        try:
            # Delete namespace
            self.index.delete(
                delete_all=True,
                namespace=f"user_{user_id}"
            )
            return True

        except Exception as e:
            print(f"Error deleting user memory: {e}")
            return False

    async def get_memory_stats(self, user_id: int) -> Dict[str, Any]:
        """
        Get statistics about user's vector memory

        Args:
            user_id: User ID

        Returns:
            Memory statistics
        """
        if not self.is_enabled():
            return {"enabled": False}

        try:
            stats = self.index.describe_index_stats()
            namespace_stats = stats.namespaces.get(f"user_{user_id}", {})

            return {
                "enabled": True,
                "vector_count": namespace_stats.get("vector_count", 0),
                "index_fullness": stats.index_fullness,
                "dimension": stats.dimension
            }

        except Exception as e:
            print(f"Error getting memory stats: {e}")
            return {"enabled": True, "error": str(e)}
