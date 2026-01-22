"""
Auth Routes - API endpoints for authentication
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import uuid
import hashlib

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """Request model for login"""
    email: str = Field(...)
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    """Request model for registration"""
    email: str = Field(...)
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Response model for authentication tokens"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str


class UserResponse(BaseModel):
    """Response model for user info"""
    user_id: str
    email: str
    name: str
    created_at: datetime


class AuthService:
    """Service class for authentication operations"""
    
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.tokens: Dict[str, Dict[str, Any]] = {}
    
    def _hash_password(self, password: str) -> str:
        """Hash password (simple for demo)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self) -> str:
        """Generate access token"""
        return f"tk_{uuid.uuid4().hex}"
    
    async def register(
        self,
        email: str,
        password: str,
        name: str
    ) -> Dict[str, Any]:
        """Register a new user"""
        # Check if email exists
        for user in self.users.values():
            if user["email"] == email:
                raise ValueError("Email already registered")
        
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        user = {
            "user_id": user_id,
            "email": email,
            "password_hash": self._hash_password(password),
            "name": name,
            "created_at": now,
        }
        
        self.users[user_id] = user
        return {
            "user_id": user_id,
            "email": email,
            "name": name,
            "created_at": now,
        }
    
    async def login(
        self,
        email: str,
        password: str
    ) -> Dict[str, Any]:
        """Login user and return token"""
        password_hash = self._hash_password(password)
        
        for user in self.users.values():
            if user["email"] == email and user["password_hash"] == password_hash:
                # Generate token
                token = self._generate_token()
                expires_at = datetime.utcnow() + timedelta(hours=24)
                
                self.tokens[token] = {
                    "user_id": user["user_id"],
                    "expires_at": expires_at,
                }
                
                return {
                    "access_token": token,
                    "token_type": "bearer",
                    "expires_in": 86400,  # 24 hours
                    "user_id": user["user_id"],
                }
        
        raise ValueError("Invalid credentials")
    
    async def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate access token"""
        if token in self.tokens:
            token_data = self.tokens[token]
            if token_data["expires_at"] > datetime.utcnow():
                user_id = token_data["user_id"]
                return self.users.get(user_id)
        return None
    
    async def logout(self, token: str) -> bool:
        """Invalidate token"""
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False


# Global service instance
_auth_service = AuthService()


def get_auth_service() -> AuthService:
    """Dependency injection for auth service"""
    return _auth_service


@router.post("/register", response_model=UserResponse)
async def register(
    request: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    try:
        result = await service.register(
            email=request.email,
            password=request.password,
            name=request.name
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    """Login and get access token"""
    try:
        result = await service.login(
            email=request.email,
            password=request.password
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout(
    token: str,
    service: AuthService = Depends(get_auth_service)
):
    """Logout and invalidate token"""
    success = await service.logout(token)
    return {"logged_out": success}
