"""
Authentication API routes
Endpoints: /login, /refresh, /logout, /register
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.core.tokens import generate_token_pair, validate_refresh_token, refresh_access_token
from app.core.security import verify_password
from app.schemas.token import LoginRequest, TokenResponse, UserCreate, UserResponse, RefreshTokenRequest
from app.models.user import User
from app.db.database import get_db

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """Login endpoint - xác thực user và trả về access token + refresh token"""
    # TODO: Implement login logic
    pass

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str = Cookie(None, alias="refresh_token"),
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token from cookie"""
    # TODO: Implement token refresh logic
    pass

@router.post("/logout")
async def logout(response: Response):
    """Logout endpoint - clear refresh token cookie"""
    # TODO: Implement logout logic
    pass

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register new user"""
    # TODO: Implement user registration logic
    pass

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user info from access token"""
    # TODO: Implement get current user logic
    pass

@router.post("/verify-token")
async def verify_token_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Verify if access token is valid"""
    # TODO: Implement token verification logic
    pass
