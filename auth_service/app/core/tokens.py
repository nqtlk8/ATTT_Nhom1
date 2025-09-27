"""
Token management utilities
Hàm tạo access/refresh token, validate tokens
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_token

def generate_token_pair(user_id: int, username: str) -> Dict[str, Any]:
    """Generate access and refresh token pair"""
    data = {
        "sub": str(user_id),
        "username": username
    }

    access_token = create_access_token(
        data,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "accessToken": access_token,
        "refreshToken": refresh_token
    }

def validate_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Validate access token and return payload"""
    # TODO: Implement access token validation
    pass

def validate_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """Validate refresh token and return payload"""
    # TODO: Implement refresh token validation
    pass

def refresh_access_token(refresh_token: str) -> Optional[str]:
    """Generate new access token from refresh token"""
    # TODO: Implement access token refresh
    pass

def revoke_token(token: str) -> bool:
    """Revoke a token (add to blacklist)"""
    # TODO: Implement token revocation
    pass

def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted"""
    # TODO: Implement blacklist check
    pass
