from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.config import settings


class TokenPayload(BaseModel):
    sub: str      # User ID
    email: str    # User email
    exp: int      # Expiration timestamp

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm=settings.algorithm)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def decode_access_token(token: str) -> Optional[TokenPayload]:
    """Decode an access token and return the payload."""
    try:
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None or email is None:
            return None

        return TokenPayload(sub=user_id, email=email, exp=payload.get("exp", 0))
    except JWTError:
        return None