"""
Security utilities for Auth Service
Hash password, verify password, tạo JWT với RSA private key
"""

from functools import lru_cache
from typing import Dict, Any
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from app.core.config import settings

# Password hashing context
# Đảm bảo bcrypt được load bằng cách import trước
try:
    import bcrypt
except ImportError:
    pass

# Khởi tạo CryptContext với bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12,
    deprecated="auto"
)

# Force load bcrypt backend ngay khi import module
try:
    # Test hash để đảm bảo bcrypt backend được load
    _ = pwd_context.hash("init_test")
except Exception:
    # Nếu lỗi, thử lại với default settings
    pass

# ==============================================================
#  Password Hashing
# ==============================================================

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt
    
    Bcrypt có giới hạn 72 bytes, nên cần đảm bảo password được encode đúng cách
    """
    # Đảm bảo password là string và encode UTF-8
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    
    # Bcrypt giới hạn 72 bytes, truncate nếu cần (hiếm khi xảy ra)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        # Đảm bảo password là string
        if isinstance(plain_password, bytes):
            plain_password = plain_password.decode('utf-8')
        
        # Bcrypt giới hạn 72 bytes, truncate nếu cần
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
        
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # Log error để debug
        print(f"Error verifying password: {e}")
        return False

# ==============================================================
#  JWT Token Creation (RSA Private Key)
# ==============================================================

@lru_cache()
def load_private_key() -> str:
    """Đọc private key từ file PEM và cache lại."""
    # Thử nhiều đường dẫn để tìm private key
    possible_paths = [
        # Đường dẫn tương đối từ working directory (Docker: /app, Local: auth_service/)
        settings.PRIVATE_KEY_PATH,
        # Đường dẫn tuyệt đối từ thư mục auth_service (local development)
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), settings.PRIVATE_KEY_PATH),
        # Đường dẫn từ thư mục hiện tại
        os.path.join(os.getcwd(), settings.PRIVATE_KEY_PATH),
        # Đường dẫn trong Docker (/app)
        os.path.join("/app", settings.PRIVATE_KEY_PATH),
    ]
    
    private_key_path = None
    for path in possible_paths:
        if os.path.exists(path):
            private_key_path = path
            break
    
    if not private_key_path:
        error_msg = f"Private key not found. Tried paths: {possible_paths}"
        raise FileNotFoundError(error_msg)
    
    try:
        with open(private_key_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise FileNotFoundError(f"Cannot read private key from {private_key_path}: {str(e)}")

def create_access_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
    """
    Tạo JWT access token sử dụng RSA private key (RS256)
    
    Args:
        data: Dictionary chứa thông tin user (sub, username, email, etc.)
        expires_delta: Thời gian hết hạn của token
    
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    # JWT yêu cầu exp và iat là int (Unix timestamp)
    from datetime import timezone
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": int(expire.timestamp()),  # Convert to Unix timestamp
        "iat": int(now.timestamp()),      # Convert to Unix timestamp
        "iss": "auth_service",            # Issuer
    })
    
    try:
        private_key = load_private_key()
    except Exception as e:
        raise ValueError(f"Không thể load private key: {str(e)}")
    
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            private_key,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        raise ValueError(f"Không thể tạo JWT token: {str(e)}")