"""
Configuration settings for Resource Service
Cấu hình database, public key path, và các settings khác
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./data/resource_service.db"
    
    # RSA Public Key path (copy từ auth_service)
    PUBLIC_KEY_PATH: str = "rsa_keys/public.pem"
    
    # JWT settings
    ALGORITHM: str = "RS256"
    
    # Security settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
