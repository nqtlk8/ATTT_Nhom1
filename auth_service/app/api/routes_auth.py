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
    # Find user by username
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Generate token pair
    token_data = generate_token_pair(user.id, user.username)
    
    # Set refresh token in HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=token_data["refresh_token"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 days in seconds
    )
    
    # Return access token in response body
    return TokenResponse(
        access_token=token_data["access_token"],
        token_type="bearer",
        expires_in=token_data["expires_in"]
    )

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
    # Clear the refresh token cookie
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )
    
    return {"message": "Successfully logged out"}

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
