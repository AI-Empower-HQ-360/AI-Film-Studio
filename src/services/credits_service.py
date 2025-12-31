"""Credits Service - Microservice for credit and subscription management"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum

class SubscriptionTier(str, Enum):
    """Subscription tier enumeration"""
    FREE = "free"
    STANDARD = "standard"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class TransactionType(str, Enum):
    """Credit transaction type enumeration"""
    PURCHASE = "purchase"
    DEDUCTION = "deduction"
    GRANT = "grant"
    REFUND = "refund"

class CreditsService:
    """
    Credits Service handles all credit and subscription-related operations including:
    - Credit balance management
    - Credit transactions
    - Subscription tier management
    - Payment processing integration
    """
    
    # Subscription tier configuration
    TIER_CONFIG = {
        SubscriptionTier.FREE: {
            "price": 0,
            "credits_per_month": 3,
            "max_duration_minutes": 1,
            "watermark": True,
            "features": ["basic_voices"]
        },
        SubscriptionTier.STANDARD: {
            "price": 9.99,
            "credits_per_month": 30,
            "max_duration_minutes": 3,
            "watermark": False,
            "features": ["standard_voices", "basic_music"]
        },
        SubscriptionTier.PRO: {
            "price": 29.99,
            "credits_per_month": 100,
            "max_duration_minutes": 5,
            "watermark": False,
            "features": ["premium_voices", "advanced_music", "priority_queue"]
        },
        SubscriptionTier.ENTERPRISE: {
            "price": 299.99,
            "credits_per_month": 999999,  # Unlimited
            "max_duration_minutes": 10,
            "watermark": False,
            "features": [
                "premium_voices", 
                "advanced_music", 
                "priority_queue",
                "white_label",
                "api_access",
                "custom_voices"
            ]
        }
    }
    
    def __init__(self, db_session, redis_client):
        self.db = db_session
        self.redis = redis_client
        
    async def get_credit_balance(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's current credit balance
        
        Args:
            user_id: User ID
            
        Returns:
            Dict containing balance, tier, reset_date, and history
        """
        # Check Redis cache first
        cache_key = f"user:credits:{user_id}"
        cached_balance = await self.redis.get(cache_key)
        
        if cached_balance:
            balance = int(cached_balance)
        else:
            # TODO: Fetch from database
            balance = 50
            # Cache for 5 minutes
            await self.redis.setex(cache_key, 300, balance)
        
        # Get transaction history
        history = await self._get_transaction_history(user_id, limit=10)
        
        return {
            "balance": balance,
            "tier": "pro",
            "reset_date": (datetime.now() + timedelta(days=15)).date().isoformat(),
            "history": history
        }
    
    async def deduct_credits(
        self,
        user_id: str,
        amount: int,
        description: str,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deduct credits from user's balance
        
        Args:
            user_id: User ID
            amount: Number of credits to deduct
            description: Description of transaction
            project_id: Optional project ID
            
        Returns:
            Dict with transaction details and new balance
            
        Raises:
            ValueError: If insufficient credits
        """
        # Get current balance
        balance_data = await self.get_credit_balance(user_id)
        current_balance = balance_data["balance"]
        
        # Check if sufficient credits
        if current_balance < amount:
            raise ValueError(f"Insufficient credits. Required: {amount}, Available: {current_balance}")
        
        # Calculate new balance
        new_balance = current_balance - amount
        
        # Create transaction record
        transaction = {
            "user_id": user_id,
            "type": TransactionType.DEDUCTION,
            "amount": -amount,
            "balance_after": new_balance,
            "description": description,
            "project_id": project_id,
            "created_at": datetime.now()
        }
        
        # TODO: Insert transaction into database
        # TODO: Update user balance in database
        
        # Update Redis cache
        cache_key = f"user:credits:{user_id}"
        await self.redis.setex(cache_key, 300, new_balance)
        
        return {
            "transaction_id": "uuid-generated",
            "balance_after": new_balance,
            "amount_deducted": amount
        }
    
    async def refund_credits(
        self,
        user_id: str,
        amount: int,
        description: str,
        original_transaction_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Refund credits to user (e.g., if job fails)
        
        Args:
            user_id: User ID
            amount: Number of credits to refund
            description: Reason for refund
            original_transaction_id: ID of original transaction
            
        Returns:
            Dict with transaction details and new balance
        """
        # Get current balance
        balance_data = await self.get_credit_balance(user_id)
        current_balance = balance_data["balance"]
        
        # Calculate new balance
        new_balance = current_balance + amount
        
        # Create transaction record
        transaction = {
            "user_id": user_id,
            "type": TransactionType.REFUND,
            "amount": amount,
            "balance_after": new_balance,
            "description": description,
            "original_transaction_id": original_transaction_id,
            "created_at": datetime.now()
        }
        
        # TODO: Insert transaction into database
        # TODO: Update user balance in database
        
        # Update Redis cache
        cache_key = f"user:credits:{user_id}"
        await self.redis.setex(cache_key, 300, new_balance)
        
        return {
            "transaction_id": "uuid-generated",
            "balance_after": new_balance,
            "amount_refunded": amount
        }
    
    async def purchase_credits(
        self,
        user_id: str,
        quantity: int,
        payment_method: str = "stripe"
    ) -> Dict[str, Any]:
        """
        Purchase additional credits
        
        Args:
            user_id: User ID
            quantity: Number of credits to purchase
            payment_method: Payment method (stripe or paypal)
            
        Returns:
            Dict with payment session info
        """
        # Credit pricing: $5 for 10 credits = $0.50 per credit
        price_per_credit = 0.50
        total_price = quantity * price_per_credit
        
        # TODO: Create Stripe payment session
        # stripe_session = create_checkout_session(...)
        
        return {
            "stripe_session_id": "cs_test_...",
            "redirect_url": "https://stripe.com/...",
            "quantity": quantity,
            "total_price": total_price
        }
    
    async def upgrade_subscription(
        self,
        user_id: str,
        new_tier: SubscriptionTier
    ) -> Dict[str, Any]:
        """
        Upgrade user's subscription tier
        
        Args:
            user_id: User ID
            new_tier: New subscription tier
            
        Returns:
            Dict with updated subscription info
        """
        tier_config = self.TIER_CONFIG[new_tier]
        
        # TODO: Create subscription in Stripe
        # TODO: Update user record in database
        
        # Reset credits to new tier allowance
        new_balance = tier_config["credits_per_month"]
        reset_date = datetime.now() + timedelta(days=30)
        
        # Update cache
        cache_key = f"user:credits:{user_id}"
        await self.redis.setex(cache_key, 300, new_balance)
        
        return {
            "subscription_tier": new_tier.value,
            "credits_per_month": tier_config["credits_per_month"],
            "price": tier_config["price"],
            "features": tier_config["features"],
            "next_billing_date": reset_date.date().isoformat()
        }
    
    async def calculate_credits_required(
        self,
        duration_minutes: float
    ) -> int:
        """
        Calculate credits required for video duration
        
        Args:
            duration_minutes: Video duration in minutes
            
        Returns:
            Number of credits required (3 credits per minute, rounded up)
        """
        import math
        minutes_rounded = math.ceil(duration_minutes)
        credits_required = minutes_rounded * 3
        return credits_required
    
    async def _get_transaction_history(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent credit transactions"""
        # TODO: Fetch from database
        return [
            {
                "date": "2025-12-20T10:30:00Z",
                "type": "deduction",
                "amount": -3,
                "description": "Film generated: My First Film"
            },
            {
                "date": "2025-12-15T14:20:00Z",
                "type": "purchase",
                "amount": 30,
                "description": "Credit purchase (10 credits)"
            }
        ]
    
    async def check_tier_limits(
        self,
        user_id: str,
        duration_minutes: float
    ) -> Dict[str, Any]:
        """
        Check if video duration is within user's tier limits
        
        Args:
            user_id: User ID
            duration_minutes: Requested video duration
            
        Returns:
            Dict with allowed status and tier limits
        """
        # TODO: Get user's tier from database
        user_tier = SubscriptionTier.PRO
        tier_config = self.TIER_CONFIG[user_tier]
        
        max_duration = tier_config["max_duration_minutes"]
        allowed = duration_minutes <= max_duration
        
        return {
            "allowed": allowed,
            "max_duration_minutes": max_duration,
            "requested_duration_minutes": duration_minutes,
            "tier": user_tier.value
        }
