"""Credit and subscription API schemas"""
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class CreditBalance(BaseModel):
    """Schema for credit balance response"""
    balance: int
    plan_type: str
    credits_per_minute: int = 3


class CreditTopup(BaseModel):
    """Schema for credit top-up request"""
    plan_type: str
    payment_method: Optional[str] = None


class PlanResponse(BaseModel):
    """Schema for subscription plan response"""
    plan_type: str
    price: float
    credits_per_month: int
    credits_per_minute: int
    max_video_length: int
    features: Optional[str]

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    """Schema for credit transaction response"""
    id: UUID
    user_id: UUID
    transaction_type: str
    amount: int
    balance_after: int
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionList(BaseModel):
    """Schema for list of transactions"""
    transactions: List[TransactionResponse]
    total: int
