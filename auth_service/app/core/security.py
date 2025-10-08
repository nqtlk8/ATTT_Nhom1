from functools import lru_cache
from typing import Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from pydantic import BaseModel

import os
from datetime import datetime

# ==============================================================
#  MODULE: core/security.py
#  Mục đích:
#     - Xác thực token JWT ký bằng RSA (verify_token)
#     - Lấy thông tin user hiện tại từ JWT (get_current_user)
#  Service: Resource Service
# ==============================================================

# --- Cấu hình hệ thống ---
PUBLIC_KEY_PATH = os.getenv("RSA_PUBLIC_KEY_PATH", "rsa_keys/public.pem")
ALGORITHM = "RS256"
ACCESS_TOKEN_AUDIENCE = None  # nếu dùng audience, đặt chuỗi ở đây

# --- Định nghĩa model cho payload ---
class TokenPayload(BaseModel):
    sub: str  # user id
    exp: int
    iat: Optional[int] = None
    iss: Optional[str] = None
    roles: Optional[list] = None
    email: Optional[str] = None


# --- Đọc public key ---
@lru_cache()
def load_public_key() -> str:
    """Đọc public key từ file PEM và cache lại."""
    with open(PUBLIC_KEY_PATH, "r", encoding="utf-8") as f:
        return f.read()


# --- Xác thực token ---
def verify_token(token: str) -> Dict:
    """Giải mã & xác thực JWT ký bằng RSA public key."""
    public_key = load_public_key()
    try:
        payload = jwt.decode(token, public_key, algorithms=[ALGORITHM], audience=ACCESS_TOKEN_AUDIENCE)
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

    if token_data.exp and datetime.utcfromtimestamp(token_data.exp) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# --- Tạo HTTPBearer dependency ---
security_scheme = HTTPBearer(auto_error=False)


# --- Hàm giả lập lấy user từ DB ---
def get_user_by_id_stub(user_id: str):
    """Placeholder: thay bằng truy vấn DB thật."""
    fake_users = {
        "1": {"id": "1", "username": "alice", "email": "alice@example.com", "roles": ["user"]},
        "2": {"id": "2", "username": "bob", "email": "bob@example.com", "roles": ["admin"]},
    }
    return fake_users.get(user_id)


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

    user = get_user_by_id_stub(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy user")

    return user
