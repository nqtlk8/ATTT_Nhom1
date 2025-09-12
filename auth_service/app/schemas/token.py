"""
Pydantic schemas for authentication
LoginRequest, TokenResponse, và các schemas khác
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str

class UserCreate(BaseModel):
    """User creation schema"""
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str

class TokenData(BaseModel):
    """Token data schema"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    exp: Optional[datetime] = None
