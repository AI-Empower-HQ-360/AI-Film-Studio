"""Seed subscription plans

This script populates the subscription_plans table with default plans
"""
import sys
import os
from uuid import uuid4

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from src.database.base import engine, SessionLocal
from src.database.models.credit import SubscriptionPlan
from src.database.models.user import PlanType


def seed_subscription_plans(db: Session):
    """Seed the subscription plans table"""
    
    # Check if plans already exist
    existing_plans = db.query(SubscriptionPlan).count()
    if existing_plans > 0:
        print(f"Subscription plans already exist ({existing_plans} plans found). Skipping seed.")
        return
    
    plans = [
        {
            "plan_type": PlanType.FREE,
            "price": 0.0,
            "credits_per_month": 3,
            "credits_per_minute": 3,
            "max_video_length": 1,
            "features": "3 credits (1 minute video), Watermarked videos, Basic support"
        },
        {
            "plan_type": PlanType.STANDARD,
            "price": 39.0,
            "credits_per_month": 30,
            "credits_per_minute": 3,
            "max_video_length": 10,
            "features": "30 credits (10 minutes video), No watermark, Priority support, HD quality"
        },
        {
            "plan_type": PlanType.PRO,
            "price": 49.0,
            "credits_per_month": 60,
            "credits_per_minute": 3,
            "max_video_length": 20,
            "features": "60 credits (20 minutes video), No watermark, Priority support, 4K quality, Advanced AI features"
        },
        {
            "plan_type": PlanType.ENTERPRISE,
            "price": 99.0,
            "credits_per_month": 120,
            "credits_per_minute": 3,
            "max_video_length": 40,
            "features": "120 credits (40 minutes video), No watermark, 24/7 support, 4K quality, Advanced AI features, Custom models, API access"
        }
    ]
    
    for plan_data in plans:
        plan = SubscriptionPlan(
            id=uuid4(),
            **plan_data
        )
        db.add(plan)
    
    db.commit()
    print(f"Successfully seeded {len(plans)} subscription plans")


if __name__ == "__main__":
    print("Seeding subscription plans...")
    db = SessionLocal()
    try:
        seed_subscription_plans(db)
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()
    print("Done!")
