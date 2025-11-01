"""
Security utilities for Resource Service
Verify JWT với RSA public key
"""

from functools import lru_cache
from typing import Dict, Optional
import os
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from app.core.config import settings

# ==============================================================
#  MODULE: core/security.py
#  Mục đích:
#     - Xác thực token JWT ký bằng RSA (verify_token)
#     - Lấy thông tin user hiện tại từ JWT (get_current_user)
#  Service: Resource Service
# ==============================================================

ALGORITHM = "RS256"

# --- Định nghĩa model cho payload ---
class TokenPayload(BaseModel):
    sub: str  # user id
    exp: int
    iat: Optional[int] = None
    iss: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None

# --- Đọc public key ---
@lru_cache()
def load_public_key() -> str:
    """Đọc public key từ file PEM và cache lại."""
    # Thử nhiều đường dẫn để tìm public key
    possible_paths = [
        # Đường dẫn tương đối từ working directory (Docker: /app, Local: resource_service/)
        settings.PUBLIC_KEY_PATH,
        # Đường dẫn tuyệt đối từ thư mục resource_service (local development)
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), settings.PUBLIC_KEY_PATH),
        # Đường dẫn từ thư mục hiện tại
        os.path.join(os.getcwd(), settings.PUBLIC_KEY_PATH),
        # Đường dẫn trong Docker (/app)
        os.path.join("/app", settings.PUBLIC_KEY_PATH),
    ]
    
    public_key_path = None
    for path in possible_paths:
        if os.path.exists(path):
            public_key_path = path
            break
    
    if not public_key_path:
        error_msg = f"Public key not found. Tried paths: {possible_paths}"
        raise FileNotFoundError(error_msg)
    
    try:
        with open(public_key_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise FileNotFoundError(f"Cannot read public key from {public_key_path}: {str(e)}")

# --- Xác thực token ---
def verify_token(token: str) -> Dict:
    """Giải mã & xác thực JWT ký bằng RSA public key."""
    public_key = load_public_key()
    try:
        payload = jwt.decode(token, public_key, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Không thể xác thực token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token_data = TokenPayload(**payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Dữ liệu token không hợp lệ: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Kiểm tra token đã hết hạn chưa (jwt.decode đã check nhưng double check)
    if token_data.exp and datetime.utcfromtimestamp(token_data.exp) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload

# --- Tạo HTTPBearer dependency ---
security_scheme = HTTPBearer(auto_error=False)

# --- Dependency FastAPI ---
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """Lấy user hiện tại từ JWT gửi trong header Authorization."""
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thiếu hoặc sai định dạng Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token thiếu trường 'sub' (user id)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Trả về thông tin user từ token
    return {
        "user_id": int(user_id),
        "username": payload.get("username", ""),
        "email": payload.get("email", ""),
    }