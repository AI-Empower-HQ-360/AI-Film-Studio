"""
Authentication API endpoints.
"""
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas import UserCreate, UserLogin, Token, TokenRefresh, UserResponse
from app.core.security import (
    verify_password, get_password_hash, 
    create_access_token, create_refresh_token, decode_token
)
from app.core.config import settings

router = APIRouter()


# Mock database for demonstration
# In production, replace with actual database operations
mock_users = {}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user."""
    # Check if user already exists
    if user_data.email in mock_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = {
        "id": len(mock_users) + 1,
        "email": user_data.email,
        "username": user_data.username,
        "hashed_password": get_password_hash(user_data.password),
        "is_active": True,
        "created_at": "2024-01-01T00:00:00"
    }
    mock_users[user_data.email] = user
    
    return UserResponse(**user)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login and get access tokens."""
    # Verify user exists
    user = mock_users.get(credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user["email"]}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user["id"]), "email": user["email"]}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh):
    """Refresh access token using refresh token."""
    try:
        payload = decode_token(token_data.refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Create new tokens
        access_token = create_access_token(
            data={"sub": payload["sub"], "email": payload.get("email")}
        )
        refresh_token = create_refresh_token(
            data={"sub": payload["sub"], "email": payload.get("email")}
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
