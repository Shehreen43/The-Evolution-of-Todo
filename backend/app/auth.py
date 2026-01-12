"""
Authentication utilities for the Full-Stack Todo Web Application.

This module provides functions for:
- Password hashing and verification
- JWT token creation and verification
- User authentication utilities
"""

from datetime import datetime, timedelta
from typing import Optional
import re
import bcrypt
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from jose.constants import ALGORITHMS

from app.config import settings
from app.models.user import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """Data contained in JWT token."""
    user_id: str
    email: str


def hash_password(password: str) -> str:
    """
    Hash a plain text password.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    # Use bcrypt to hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password

    Returns:
        True if passwords match, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_jwt_token(user_id: str, email: str) -> str:
    """
    Create a JWT token for a user.

    Args:
        user_id: User's unique identifier
        email: User's email address

    Returns:
        Encoded JWT token string
    """
    # Set token expiration
    expire = datetime.utcnow() + timedelta(days=settings.jwt_expiration_days)

    # Create token payload
    to_encode = {
        "sub": user_id,
        "email": email,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp(),
        "type": "access"
    }

    # Encode the token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.better_auth_secret,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_jwt_token(token: str) -> Optional[TokenData]:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT token string

    Returns:
        TokenData containing user information if valid, None otherwise
    """
    try:
        # Decode the token
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.algorithm]
        )

        # Extract user information
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None or email is None:
            return None

        # Check if token is expired
        exp_timestamp = payload.get("exp")
        if exp_timestamp and datetime.fromtimestamp(exp_timestamp) < datetime.utcnow():
            return None

        return TokenData(user_id=user_id, email=email)
    except JWTError:
        # Token is invalid or malformed
        return None


def get_current_user(token: str) -> Optional[User]:
    """
    Get the current user from a JWT token.

    Args:
        token: JWT token string

    Returns:
        User object if token is valid and user exists, None otherwise
    """
    # This function would typically query the database to get user info
    # For now, it returns the decoded token data
    token_data = decode_jwt_token(token)
    if token_data is None:
        return None

    # In a real implementation, you would fetch the user from the database
    # For this example, we return a basic User object with just the ID and email
    return User(
        id=token_data.user_id,
        email=token_data.email,
        name="",  # Would be fetched from database
        password_hash=""  # Would never be returned in a real implementation
    )


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength requirements.

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        # Note: The spec doesn't require special characters, but it's good practice
        pass  # Not required by spec, so we don't enforce it here

    return True, ""