"""Credit and subscription models"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey, func, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from src.database.base import Base
from src.database.models.user import PlanType


class Credit(Base):
    """
    Credits / Plans Table
    Stores user credit balance and subscription information
    """
    __tablename__ = "credits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_type = Column(Enum(PlanType), nullable=False)
    credits_balance = Column(Integer, default=0, nullable=False)
    subscription_start = Column(DateTime(timezone=True), nullable=True)
    subscription_end = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="credit_records")

    def __repr__(self):
        return f"<Credit(id={self.id}, user_id={self.user_id}, balance={self.credits_balance})>"


class TransactionType(str, enum.Enum):
    """Credit transaction types"""
    DEDUCTION = "deduction"
    PURCHASE = "purchase"
    GRANT = "grant"
    REFUND = "refund"


class CreditTransaction(Base):
    """
    Credit Transactions Table
    Records all credit changes for audit and history
    """
    __tablename__ = "credit_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Integer, nullable=False)  # Can be negative for deductions
    balance_after = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="credit_transactions")

    def __repr__(self):
        return f"<CreditTransaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"


class SubscriptionPlan(Base):
    """
    Subscription Plans Table
    Stores available subscription plans with pricing
    """
    __tablename__ = "subscription_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    plan_type = Column(Enum(PlanType), unique=True, nullable=False)
    price = Column(Float, nullable=False)  # Price in USD
    credits_per_month = Column(Integer, nullable=False)
    credits_per_minute = Column(Integer, default=3, nullable=False)  # 3 credits = 1 minute
    max_video_length = Column(Integer, nullable=False)  # Maximum video length in minutes
    features = Column(String(1000), nullable=True)  # JSON string of features
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<SubscriptionPlan(plan_type={self.plan_type}, price={self.price})>"
