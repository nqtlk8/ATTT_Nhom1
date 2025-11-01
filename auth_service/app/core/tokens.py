"""
Token management utilities
Hàm tạo access token, validate tokens
"""

from datetime import timedelta
from typing import Dict, Any
from app.core.config import settings
from app.core.security import create_access_token

def generate_access_token(user_id: int, username: str, email: str = None) -> Dict[str, Any]:
    """
    Generate access token only (không cần refresh token)
    
    Args:
        user_id: User ID
        username: Username
        email: Email (optional)
    
    Returns:
        Dictionary chứa access_token, token_type, expires_in
    """
    # Tạo payload cho JWT
    token_data = {
        "sub": str(user_id),  # Subject (user id)
        "username": username,
    }
    
    if email:
        token_data["email"] = email
    
    # Tạo token với thời gian hết hạn
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=token_data, expires_delta=expires_delta)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # seconds
    }
