"""
Product API routes
Endpoints: /products (cần JWT authentication)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.security import verify_jwt_token, get_current_user_from_token
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse, UserInfo
from app.models.product import Product
from app.db.database import get_db

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserInfo:
    """Dependency to get current user from JWT token"""
    # TODO: Implement current user extraction from JWT
    pass

@router.get("/products", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of products (requires JWT authentication)"""
    # TODO: Implement get products logic
    pass

@router.post("/products", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    current_user: UserInfo = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new product (requires JWT authentication)"""
    # TODO: Implement create product logic
    pass
