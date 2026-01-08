"""
User Service - Handles user authentication, registration, and profile management
"""
from typing import Optional, Dict
from datetime import datetime, timedelta
import jwt
from passlib.hash import bcrypt
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class UserService:
    """Service for managing user operations"""
    
    def __init__(self, db_connection, jwt_secret: str, jwt_algorithm: str = "HS256"):
        self.db = db_connection
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.token_expiry = timedelta(hours=24)
        self.refresh_token_expiry = timedelta(days=7)
    
    async def register_user(
        self,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        tier: str = "free"
    ) -> Dict:
        """
        Register a new user
        
        Args:
            email: User email address
            password: Plain text password
            first_name: User first name
            last_name: User last name
            tier: User subscription tier (free, pro, enterprise)
            
        Returns:
            Dict containing user information and tokens
        """
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Hash password
            password_hash = bcrypt.hash(password)
            
            # Create user in database
            user_data = {
                "email": email,
                "password_hash": password_hash,
                "first_name": first_name,
                "last_name": last_name,
                "tier": tier,
                "credits": self._get_initial_credits(tier),
                "email_verified": False,
                "is_active": True
            }
            
            user_id = await self.db.insert("users", user_data)
            
            # Generate tokens
            access_token = self._generate_access_token(user_id, email, tier)
            refresh_token = self._generate_refresh_token(user_id)
            
            logger.info(f"User registered successfully: {email}")
            
            return {
                "user_id": user_id,
                "email": email,
                "tier": tier,
                "credits": user_data["credits"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            
        except Exception as e:
            logger.error(f"Error registering user: {str(e)}")
            raise
    
    async def login(self, email: str, password: str) -> Dict:
        """
        Authenticate user and generate tokens
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Dict containing user info and tokens
        """
        try:
            # Get user from database
            user = await self.get_user_by_email(email)
            
            if not user:
                raise ValueError("Invalid email or password")
            
            # Verify password
            if not bcrypt.verify(password, user["password_hash"]):
                raise ValueError("Invalid email or password")
            
            # Check if user is active
            if not user["is_active"]:
                raise ValueError("Account is deactivated")
            
            # Update last login
            await self.db.update(
                "users",
                {"id": user["id"]},
                {"last_login_at": datetime.utcnow()}
            )
            
            # Generate tokens
            access_token = self._generate_access_token(
                user["id"], user["email"], user["tier"]
            )
            refresh_token = self._generate_refresh_token(user["id"])
            
            logger.info(f"User logged in: {email}")
            
            return {
                "user_id": user["id"],
                "email": user["email"],
                "tier": user["tier"],
                "credits": user["credits"],
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": int(self.token_expiry.total_seconds())
            }
            
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email address"""
        try:
            users = await self.db.query(
                "SELECT * FROM users WHERE email = %s AND deleted_at IS NULL",
                (email,)
            )
            return users[0] if users else None
        except Exception as e:
            logger.error(f"Error fetching user by email: {str(e)}")
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            users = await self.db.query(
                "SELECT * FROM users WHERE id = %s AND deleted_at IS NULL",
                (user_id,)
            )
            return users[0] if users else None
        except Exception as e:
            logger.error(f"Error fetching user by ID: {str(e)}")
            raise
    
    async def update_user_profile(
        self,
        user_id: str,
        updates: Dict
    ) -> Dict:
        """
        Update user profile information
        
        Args:
            user_id: User ID
            updates: Dictionary of fields to update
            
        Returns:
            Updated user information
        """
        try:
            # Allowed fields for update
            allowed_fields = [
                "first_name", "last_name", "avatar_url", "locale"
            ]
            
            # Filter updates to allowed fields only
            filtered_updates = {
                k: v for k, v in updates.items() if k in allowed_fields
            }
            
            if not filtered_updates:
                raise ValueError("No valid fields to update")
            
            await self.db.update("users", {"id": user_id}, filtered_updates)
            
            # Return updated user
            user = await self.get_user_by_id(user_id)
            logger.info(f"User profile updated: {user_id}")
            
            return user
            
        except Exception as e:
            logger.error(f"Error updating user profile: {str(e)}")
            raise
    
    async def change_password(
        self,
        user_id: str,
        old_password: str,
        new_password: str
    ) -> bool:
        """Change user password"""
        try:
            user = await self.get_user_by_id(user_id)
            
            if not user:
                raise ValueError("User not found")
            
            # Verify old password
            if not bcrypt.verify(old_password, user["password_hash"]):
                raise ValueError("Invalid current password")
            
            # Hash new password
            new_password_hash = bcrypt.hash(new_password)
            
            # Update password
            await self.db.update(
                "users",
                {"id": user_id},
                {"password_hash": new_password_hash}
            )
            
            logger.info(f"Password changed for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error changing password: {str(e)}")
            raise
    
    async def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return None
    
    def _generate_access_token(
        self,
        user_id: str,
        email: str,
        tier: str
    ) -> str:
        """Generate JWT access token"""
        payload = {
            "user_id": user_id,
            "email": email,
            "tier": tier,
            "type": "access",
            "exp": datetime.utcnow() + self.token_expiry,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def _generate_refresh_token(self, user_id: str) -> str:
        """Generate JWT refresh token"""
        payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": datetime.utcnow() + self.refresh_token_expiry,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def _get_initial_credits(self, tier: str) -> int:
        """Get initial credits based on user tier"""
        credit_map = {
            "free": 3,
            "pro": 30,
            "enterprise": 999999,
            "admin": 999999
        }
        return credit_map.get(tier, 3)
