"""Log model"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.base import Base


class Log(Base):
    """
    Logs Table
    Stores system logs and user actions for audit trail
    """
    __tablename__ = "logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    action = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="logs")
    project = relationship("Project", back_populates="logs")

    def __repr__(self):
        return f"<Log(id={self.id}, action={self.action}, timestamp={self.timestamp})>"
