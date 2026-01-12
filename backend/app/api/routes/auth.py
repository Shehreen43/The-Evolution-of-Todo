"""
Authentication API routes for the Full-Stack Todo Web Application.

This module implements:
- User registration (signup)
- User login (signin)
- User profile retrieval
- Token-based authentication
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr
from typing import Optional
import re
import re
import uuid
from app.utils.jwt import create_access_token, get_password_hash, verify_password, TokenPayload, decode_access_token

from app.models.user import User
from app.database.connection import get_db
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


router = APIRouter(prefix="/api/auth", tags=["auth"])


# Pydantic models for authentication
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str


class TokenResponse(BaseModel):
    user: UserResponse
    token: str
    expires_at: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Helper functions removed in favor of app.utils.jwt


def validate_email_format(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, ""


# HTTP Bearer security for protected routes
security = HTTPBearer()


@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user account."""
    # Validate email format
    if not validate_email_format(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password strength
    is_valid, error_msg = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Check if user already exists
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        id=str(uuid.uuid4()),  # Use UUID4
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_password
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Create JWT token
    token = create_access_token(
        data={"sub": user.id, "email": user.email, "type": "access"},
        expires_delta=timedelta(days=settings.jwt_expiration_days)
    )

    # Calculate expiration time
    expires_at = (datetime.utcnow() + timedelta(days=settings.jwt_expiration_days)).isoformat()

    return TokenResponse(
        user=UserResponse(id=user.id, email=user.email, name=user.name),
        token=token,
        expires_at=expires_at
    )


@router.post("/signin", response_model=TokenResponse)
async def signin(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token."""
    # Find user by email
    result = await db.execute(select(User).filter(User.email == login_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    token = create_access_token(
        data={"sub": user.id, "email": user.email, "type": "access"},
        expires_delta=timedelta(days=settings.jwt_expiration_days)
    )

    # Calculate expiration time
    expires_at = (datetime.utcnow() + timedelta(days=settings.jwt_expiration_days)).isoformat()

    return TokenResponse(
        user=UserResponse(id=user.id, email=user.email, name=user.name),
        token=token,
        expires_at=expires_at
    )


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    """Get the current user from a JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token
        payload = decode_access_token(token.credentials)
        if payload is None:
            raise credentials_exception
            
        user_id = payload.sub
        
    except Exception:
        raise credentials_exception

    # Get user from database
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name
    )


@router.post("/logout")
async def logout():
    """Logout user (client-side token invalidation)."""
    return {"message": "Logged out successfully"}