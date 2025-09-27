"""
Configuration settings for Auth Service
Cấu hình database, key paths, TTL, và các settings khác
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./data/auth_service.db"
    
    # RSA Key paths
    PRIVATE_KEY_PATH: str = "auth_service/rsa_keys/private.pem"
    PUBLIC_KEY_PATH: str = "auth_service/rsa_keys/public.pem"
    
    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "RS256"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8001"]
    
    # Cookie settings
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    COOKIE_SECURE: bool = False  # Set to True in production
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
