"""
Pydantic schemas for authentication
LoginRequest, TokenResponse, và các schemas khác
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str = Field(..., min_length=1, max_length=100)

class UserCreate(BaseModel):
    """User creation schema"""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=100)
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        """Đảm bảo password không quá 72 bytes (giới hạn của bcrypt)"""
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError('Password quá dài (tối đa 72 bytes)')
        return v

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

