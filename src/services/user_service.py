"""User Service - Microservice for user management"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """
    User Service handles all user-related operations including:
    - User registration and authentication
    - Profile management
    - Password reset and email verification
    - Role-based access control (RBAC)
    """
    
    def __init__(self, db_session, redis_client):
        self.db = db_session
        self.redis = redis_client
        self.secret_key = "your-secret-key"  # Should be from environment variable
        
    async def register_user(
        self, 
        email: str, 
        password: str, 
        full_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            email: User email address
            password: User password (will be hashed)
            full_name: User's full name
            
        Returns:
            Dict containing user_id, email, and subscription_tier
        """
        # Hash password
        password_hash = pwd_context.hash(password)
        
        # Create user record
        user = {
            "email": email,
            "password_hash": password_hash,
            "full_name": full_name,
            "subscription_tier": "free",
            "credits_balance": 3,  # Free tier starts with 3 credits
            "credits_reset_date": datetime.now() + timedelta(days=30),
            "created_at": datetime.now()
        }
        
        # TODO: Insert into database
        # user_id = await self.db.insert("users", user)
        
        return {
            "user_id": "uuid-generated",
            "email": email,
            "tier": "free"
        }
    
    async def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and return JWT tokens
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dict containing access_token, refresh_token, and expiry
        """
        # TODO: Fetch user from database
        # user = await self.db.get_user_by_email(email)
        
        # Verify password
        # if not pwd_context.verify(password, user["password_hash"]):
        #     raise ValueError("Invalid credentials")
        
        # Generate JWT tokens
        access_token = self._generate_access_token(email)
        refresh_token = self._generate_refresh_token(email)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 86400  # 24 hours
        }
    
    async def forgot_password(self, email: str) -> Dict[str, str]:
        """
        Send password reset link to user's email
        
        Args:
            email: User email
            
        Returns:
            Dict with status message
        """
        # TODO: Generate reset token
        # TODO: Send email with reset link
        
        return {"message": "Reset link sent"}
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get user profile information
        
        Args:
            user_id: User ID
            
        Returns:
            Dict containing user profile data
        """
        # TODO: Fetch from database
        return {
            "user_id": user_id,
            "email": "user@example.com",
            "full_name": "John Doe",
            "subscription_tier": "pro",
            "credits_balance": 50,
            "created_at": datetime.now().isoformat()
        }
    
    async def update_user_profile(
        self, 
        user_id: str, 
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            user_id: User ID
            updates: Dict of fields to update
            
        Returns:
            Updated user profile
        """
        # TODO: Update database
        return {"message": "Profile updated"}
    
    def _generate_access_token(self, email: str) -> str:
        """Generate JWT access token"""
        payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def _generate_refresh_token(self, email: str) -> str:
        """Generate JWT refresh token"""
        payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
