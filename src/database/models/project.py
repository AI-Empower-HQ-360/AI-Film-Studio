"""Project model"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Text, Integer, Enum, DateTime, JSON, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum

from src.database.base import Base


class ProjectStatus(str, enum.Enum):
    """Project status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"


class VoiceOption(str, enum.Enum):
    """Voice options for video generation"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class Project(Base):
    """
    Projects Table
    Stores user projects with scripts, images, and video generation details
    """
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    script = Column(Text, nullable=True)
    images = Column(JSON, nullable=True)  # Array of uploaded character images
    voice = Column(Enum(VoiceOption), nullable=True)
    duration = Column(Integer, nullable=True)  # Video length in minutes
    music = Column(String(255), nullable=True)  # Music/sloka selection
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PENDING, nullable=False)
    video_url = Column(String(500), nullable=True)  # S3 URL of generated video
    subtitles_url = Column(String(500), nullable=True)  # S3 URL of generated subtitles
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="projects")
    youtube_integrations = relationship("YouTubeIntegration", back_populates="project", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, title={self.title}, status={self.status})>"
