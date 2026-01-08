"""Credit and subscription service API routes"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.database.models.user import User, PlanType
from src.database.models.credit import SubscriptionPlan, CreditTransaction, TransactionType
from src.api.schemas.credit import CreditBalance, CreditTopup, PlanResponse, TransactionResponse, TransactionList
from src.utils.auth import get_current_user

router = APIRouter(prefix="/api/credits", tags=["Credits"])


@router.get("/balance", response_model=CreditBalance)
async def get_credit_balance(current_user: User = Depends(get_current_user)):
    """
    Get user's current credit balance
    
    Response:
    - balance: integer
    - plan_type: string
    - credits_per_minute: integer
    """
    return {
        "balance": current_user.credits,
        "plan_type": current_user.plan_type.value,
        "credits_per_minute": 3
    }


@router.post("/topup", response_model=dict)
async def topup_credits(
    topup_data: CreditTopup,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Top up credits / upgrade subscription plan
    
    Request:
    - plan_type: string (Free, Standard, Pro, Enterprise)
    
    Response:
    - credits_balance: integer
    - subscription_end: timestamp
    """
    # Get plan details
    plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.plan_type == topup_data.plan_type
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    
    # Update user credits and plan
    current_user.credits += plan.credits_per_month
    current_user.plan_type = topup_data.plan_type
    
    # Create transaction record
    transaction = CreditTransaction(
        user_id=current_user.id,
        transaction_type=TransactionType.PURCHASE,
        amount=plan.credits_per_month,
        balance_after=current_user.credits,
        description=f"Purchased {topup_data.plan_type} plan"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(current_user)
    
    return {
        "credits_balance": current_user.credits,
        "plan_type": current_user.plan_type.value,
        "message": "Credits topped up successfully"
    }


@router.get("/plans", response_model=List[PlanResponse])
async def get_plans(db: Session = Depends(get_db)):
    """
    Get all available subscription plans
    
    Response:
    - Array of plan objects with:
      - plan_type: string
      - price: float
      - credits_per_month: integer
      - credits_per_minute: integer
      - max_video_length: integer
      - features: string
    """
    plans = db.query(SubscriptionPlan).all()
    return plans


@router.get("/transactions", response_model=TransactionList)
async def get_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's credit transaction history
    
    Response:
    - transactions: array of transaction objects
    - total: integer
    """
    transactions = db.query(CreditTransaction).filter(
        CreditTransaction.user_id == current_user.id
    ).order_by(CreditTransaction.created_at.desc()).limit(50).all()
    
    return {
        "transactions": transactions,
        "total": len(transactions)
    }
