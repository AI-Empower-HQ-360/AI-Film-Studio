"""YouTube integration model"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from src.database.base import Base


class UploadStatus(str, enum.Enum):
    """Upload status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"


class YouTubeIntegration(Base):
    """
    YouTube Integration Table
    Stores information about YouTube uploads and integrations
    """
    __tablename__ = "youtube_integrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    channel_id = Column(String(255), nullable=True)
    video_id = Column(String(255), nullable=True)
    playlist_id = Column(String(255), nullable=True)
    upload_status = Column(Enum(UploadStatus), default=UploadStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="youtube_integrations")
    project = relationship("Project", back_populates="youtube_integrations")

    def __repr__(self):
        return f"<YouTubeIntegration(id={self.id}, video_id={self.video_id}, status={self.upload_status})>"
