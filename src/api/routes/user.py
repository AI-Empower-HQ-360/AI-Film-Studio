"""User service API routes"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.base import get_db
from src.database.models.user import User
from src.api.schemas.user import UserCreate, UserLogin, UserResponse, UserProfile, Token
from src.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    Request:
    - name: string
    - email: string (valid email format)
    - password: string (min 8 characters)
    
    Response:
    - id: UUID
    - name: string
    - email: string
    - plan_type: string
    - credits: integer
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        credits=3,  # Free tier gets 3 credits
        plan_type="Free"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user
    
    Request:
    - email: string
    - password: string
    
    Response:
    - access_token: string (JWT)
    - refresh_token: string (JWT)
    - token_type: string
    - expires_in: integer (seconds)
    """
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get user profile
    
    Headers:
    - Authorization: Bearer <token>
    
    Response:
    - id: UUID
    - name: string
    - email: string
    - plan_type: string
    - credits: integer
    - role: string
    - created_at: timestamp
    - updated_at: timestamp
    """
    return current_user
