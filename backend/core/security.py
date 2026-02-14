"""
Security utilities for JWT token handling and API key encryption.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from backend.core.config import settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """JWT token payload."""
    user_id: str
    username: str
    exp: datetime


def create_access_token(user_id: str, username: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        user_id: User identifier
        username: Username
        expires_delta: Token expiration time delta
        
    Returns:
        Encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    
    to_encode = {
        "user_id": user_id,
        "username": username,
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def verify_jwt_token(token: str) -> Optional[TokenData]:
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        TokenData if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        user_id: str = payload.get("user_id")
        username: str = payload.get("username")
        
        if user_id is None or username is None:
            return None
        
        return TokenData(
            user_id=user_id,
            username=username,
            exp=datetime.fromtimestamp(payload.get("exp"))
        )
    except JWTError as e:
        logger.warning(f"Invalid JWT token: {e}")
        return None


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)
