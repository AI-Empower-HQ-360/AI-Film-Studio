"""User model"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from src.database.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    CREATOR = "creator"
    ADMIN = "admin"


class PlanType(str, enum.Enum):
    """Subscription plan types"""
    FREE = "Free"
    STANDARD = "Standard"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"


class User(Base):
    """
    Users Table
    Stores user account information, credentials, and subscription details
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CREATOR, nullable=False)
    credits = Column(Integer, default=3, nullable=False)
    plan_type = Column(Enum(PlanType), default=PlanType.FREE, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    credit_records = relationship("Credit", back_populates="user", cascade="all, delete-orphan")
    credit_transactions = relationship("CreditTransaction", back_populates="user", cascade="all, delete-orphan")
    youtube_integrations = relationship("YouTubeIntegration", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, plan_type={self.plan_type})>"
