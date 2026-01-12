from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema."""
    email: str
    name: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

class UserResponse(BaseModel):
    """Schema for user API responses."""
    id: str
    email: str
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Schema for user login."""
    email: str
    password: str

class TokenResponse(BaseModel):
    """Schema for JWT token responses."""
    access_token: str
    token_type: str
    expires_at: datetime

    class Config:
        from_attributes = True