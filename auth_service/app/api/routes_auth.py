"""
Authentication API routes
Endpoints: /login, /register
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.tokens import generate_access_token
from app.core.security import verify_password, get_password_hash
from app.schemas.token import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.models.user import User
from app.db.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register new user
    
    - **username**: Tên đăng nhập (unique)
    - **email**: Email (unique)
    - **password**: Mật khẩu
    """
    # Kiểm tra username đã tồn tại chưa
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã tồn tại"
        )
    
    # Kiểm tra email đã tồn tại chưa
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )
    
    # Tạo user mới
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint - xác thực user và trả về access token
    
    - **username**: Tên đăng nhập hoặc email
    - **password**: Mật khẩu
    
    Returns:
    - **access_token**: JWT token (RS256 với RSA private key)
    - **token_type**: "bearer"
    - **expires_in**: Thời gian hết hạn (seconds)
    """
    try:
        # Tìm user theo username hoặc email
        user = db.query(User).filter(
            (User.username == login_data.username) | (User.email == login_data.username)
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username hoặc password không đúng",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Kiểm tra user có active không
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản đã bị vô hiệu hóa"
            )
        
        # Verify password
        try:
            password_valid = verify_password(login_data.password, user.hashed_password)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Lỗi xác thực password: {str(e)}"
            )
        
        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username hoặc password không đúng",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Tạo access token
        try:
            token_data = generate_access_token(
                user_id=user.id,
                username=user.username,
                email=user.email
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Lỗi tạo token: {str(e)}"
            )
        
        return token_data
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi đăng nhập: {str(e)}"
        )
