"""
Credits Service - Handles credit management and transactions
"""
from typing import Dict, List, Optional
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CreditsService:
    """Service for managing user credits"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def get_user_credits(self, user_id: str) -> Dict:
        """
        Get user's current credit balance
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with credit information
        """
        try:
            users = await self.db.query(
                "SELECT credits, credit_reset_date, tier FROM users WHERE id = %s",
                (user_id,)
            )
            
            if not users:
                raise ValueError("User not found")
            
            user = users[0]
            
            return {
                "balance": user["credits"],
                "tier": user["tier"],
                "reset_date": user["credit_reset_date"].isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching user credits: {str(e)}")
            raise
    
    async def deduct_credits(
        self,
        user_id: str,
        amount: int,
        description: str,
        project_id: Optional[str] = None,
        job_id: Optional[str] = None
    ) -> Dict:
        """
        Deduct credits from user account
        
        Args:
            user_id: User ID
            amount: Number of credits to deduct (positive number)
            description: Transaction description
            project_id: Optional project ID
            job_id: Optional job ID
            
        Returns:
            Transaction information
        """
        try:
            # Get current balance
            user = await self.db.query(
                "SELECT credits FROM users WHERE id = %s",
                (user_id,)
            )
            
            if not user:
                raise ValueError("User not found")
            
            current_balance = user[0]["credits"]
            
            # Check if sufficient credits
            if current_balance < amount:
                raise ValueError("Insufficient credits")
            
            new_balance = current_balance - amount
            
            # Update user credits
            await self.db.update(
                "users",
                {"id": user_id},
                {"credits": new_balance}
            )
            
            # Record transaction
            transaction_data = {
                "user_id": user_id,
                "type": "deduction",
                "amount": -amount,
                "balance_before": current_balance,
                "balance_after": new_balance,
                "description": description,
                "project_id": project_id,
                "job_id": job_id
            }
            
            transaction_id = await self.db.insert(
                "credit_transactions",
                transaction_data
            )
            
            logger.info(f"Credits deducted: {amount} from user {user_id}")
            
            return {
                "transaction_id": transaction_id,
                "amount": -amount,
                "balance_after": new_balance
            }
            
        except Exception as e:
            logger.error(f"Error deducting credits: {str(e)}")
            raise
    
    async def add_credits(
        self,
        user_id: str,
        amount: int,
        description: str,
        transaction_type: str = "purchase",
        payment_id: Optional[str] = None,
        payment_provider: Optional[str] = None,
        payment_amount: Optional[float] = None,
        payment_currency: Optional[str] = None
    ) -> Dict:
        """
        Add credits to user account
        
        Args:
            user_id: User ID
            amount: Number of credits to add
            description: Transaction description
            transaction_type: Type (purchase, grant, refund)
            payment_id: Payment transaction ID
            payment_provider: Payment provider name
            payment_amount: Payment amount in currency
            payment_currency: Currency code (USD, EUR, etc.)
            
        Returns:
            Transaction information
        """
        try:
            # Get current balance
            user = await self.db.query(
                "SELECT credits FROM users WHERE id = %s",
                (user_id,)
            )
            
            if not user:
                raise ValueError("User not found")
            
            current_balance = user[0]["credits"]
            new_balance = current_balance + amount
            
            # Update user credits
            await self.db.update(
                "users",
                {"id": user_id},
                {"credits": new_balance}
            )
            
            # Record transaction
            transaction_data = {
                "user_id": user_id,
                "type": transaction_type,
                "amount": amount,
                "balance_before": current_balance,
                "balance_after": new_balance,
                "description": description,
                "payment_id": payment_id,
                "payment_provider": payment_provider,
                "payment_amount": payment_amount,
                "payment_currency": payment_currency
            }
            
            transaction_id = await self.db.insert(
                "credit_transactions",
                transaction_data
            )
            
            logger.info(f"Credits added: {amount} to user {user_id}")
            
            return {
                "transaction_id": transaction_id,
                "amount": amount,
                "balance_after": new_balance
            }
            
        except Exception as e:
            logger.error(f"Error adding credits: {str(e)}")
            raise
    
    async def get_transaction_history(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get user's credit transaction history
        
        Args:
            user_id: User ID
            limit: Number of transactions to return
            offset: Pagination offset
            
        Returns:
            List of transactions
        """
        try:
            transactions = await self.db.query(
                """
                SELECT * FROM credit_transactions 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
                """,
                (user_id, limit, offset)
            )
            
            return transactions
            
        except Exception as e:
            logger.error(f"Error fetching transaction history: {str(e)}")
            raise
    
    async def check_sufficient_credits(
        self,
        user_id: str,
        required_amount: int
    ) -> bool:
        """
        Check if user has sufficient credits
        
        Args:
            user_id: User ID
            required_amount: Required credit amount
            
        Returns:
            True if user has sufficient credits
        """
        try:
            user = await self.db.query(
                "SELECT credits FROM users WHERE id = %s",
                (user_id,)
            )
            
            if not user:
                return False
            
            return user[0]["credits"] >= required_amount
            
        except Exception as e:
            logger.error(f"Error checking credits: {str(e)}")
            raise
    
    async def reset_monthly_credits(self, user_id: str) -> Dict:
        """
        Reset user credits based on their tier (monthly)
        
        Args:
            user_id: User ID
            
        Returns:
            Updated credit information
        """
        try:
            user = await self.db.query(
                "SELECT tier, credits FROM users WHERE id = %s",
                (user_id,)
            )
            
            if not user:
                raise ValueError("User not found")
            
            tier = user[0]["tier"]
            current_credits = user[0]["credits"]
            
            # Determine new credit amount based on tier
            credit_map = {
                "free": 3,
                "pro": 30,
                "enterprise": 999999
            }
            
            new_credits = credit_map.get(tier, 3)
            
            # Update credits and reset date
            await self.db.update(
                "users",
                {"id": user_id},
                {
                    "credits": new_credits,
                    "credit_reset_date": datetime.utcnow() + timedelta(days=30)
                }
            )
            
            # Record transaction
            transaction_data = {
                "user_id": user_id,
                "type": "reset",
                "amount": new_credits - current_credits,
                "balance_before": current_credits,
                "balance_after": new_credits,
                "description": "Monthly credit reset"
            }
            
            await self.db.insert("credit_transactions", transaction_data)
            
            logger.info(f"Credits reset for user {user_id}: {new_credits}")
            
            return {
                "balance": new_credits,
                "tier": tier
            }
            
        except Exception as e:
            logger.error(f"Error resetting credits: {str(e)}")
            raise
