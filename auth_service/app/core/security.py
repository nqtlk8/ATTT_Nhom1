"""
Security utilities for Auth Service
Load private key, ký JWT, hash passwords
"""

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def load_private_key() -> str:
    """Load private key from file"""
    with open(settings.PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

def load_public_key() -> str:
    """Load public key from file"""
    with open(settings.PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )

def generate_rsa_keypair() -> tuple:
    """Generate RSA key pair"""
    # TODO: Implement RSA key pair generation
    pass

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    # TODO: Implement password verification
    pass

def get_password_hash(password: str) -> str:
    """Hash a password"""
    # TODO: Implement password hashing
    pass

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token signed with private key"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "type": "access",
        "exp": expire,
        "iat": datetime.utcnow()
    })

    private_key = load_private_key()  # trả về object RSA
    return jwt.encode(to_encode, private_key, algorithm="RS256")

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token signed with private key"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({
        "type": "refresh",
        "exp": expire,
        "iat": datetime.utcnow()
    })

    private_key = load_private_key()  # trả về object RSA
    return jwt.encode(to_encode, private_key, algorithm="RS256")

def verify_token(token: str) -> dict:
    """Verify JWT token with public key"""
    # TODO: Implement JWT token verification
    pass
