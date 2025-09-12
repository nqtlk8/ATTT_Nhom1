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

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def load_private_key() -> str:
    """Load private key from file"""
    # TODO: Implement loading private key from file
    pass

def load_public_key() -> str:
    """Load public key from file"""
    # TODO: Implement loading public key from file
    pass

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
    # TODO: Implement JWT access token creation
    pass

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT refresh token signed with private key"""
    # TODO: Implement JWT refresh token creation
    pass

def verify_token(token: str) -> dict:
    """Verify JWT token with public key"""
    # TODO: Implement JWT token verification
    pass
