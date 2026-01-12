"""
Reading models - Coffee, Tarot, Palm readings
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class ReadingType(str, enum.Enum):
    """Types of readings available"""
    COFFEE = "coffee"
    TAROT = "tarot"
    PALM = "palm"


class Reading(Base):
    """
    Reading model - stores all types of mystical readings
    """
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Reading type
    type = Column(SQLEnum(ReadingType), nullable=False, index=True)

    # Input data (JSON) - stores user's input
    # For coffee: {"images": ["url1", "url2", "url3"]}
    # For tarot: {"spread": "celtic_cross", "cards": [{"name": "The Fool", "position": 1, "reversed": false}]}
    # For palm: {"image": "url", "hand": "right"}
    input_data = Column(JSON, nullable=False)

    # AI-generated reading text
    ai_response = Column(Text, nullable=False)

    # Detected symbols/patterns (JSON)
    # For coffee: [{"symbol": "bird", "position": "top-right", "clarity": 8}]
    # For tarot: Included in input_data
    # For palm: [{"line": "heart_line", "length": "long", "depth": "deep"}]
    symbols_detected = Column(JSON, nullable=True)

    # User feedback
    rating = Column(Integer, nullable=True)  # 1-5 stars
    feedback_text = Column(Text, nullable=True)

    # Performance metrics
    processing_time_ms = Column(Integer, nullable=True)  # Time to generate reading

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="readings")
    images = relationship("ReadingImage", back_populates="reading", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Reading(id={self.id}, type={self.type}, user_id={self.user_id})>"


class ReadingImage(Base):
    """
    Reading images - stores uploaded images for readings
    """
    __tablename__ = "reading_images"

    id = Column(Integer, primary_key=True, index=True)
    reading_id = Column(Integer, ForeignKey("readings.id"), nullable=False, index=True)

    # S3 URL or local path
    image_url = Column(String, nullable=False)

    # Image type (for coffee: cup, saucer, side; for palm: left_hand, right_hand)
    image_type = Column(String(50), nullable=True)

    # Image metadata
    file_size = Column(Integer, nullable=True)  # bytes
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    # Annotated image URL (with symbols highlighted)
    annotated_url = Column(String, nullable=True)

    # Timestamp
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    reading = relationship("Reading", back_populates="images")

    def __repr__(self):
        return f"<ReadingImage(id={self.id}, reading_id={self.reading_id}, type={self.image_type})>"
