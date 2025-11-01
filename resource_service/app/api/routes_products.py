"""
Product API routes
Endpoints: /products (cần JWT authentication)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.security import get_current_user
from app.schemas.product import ProductResponse, ProductListResponse
from app.models.product import Product
from app.db.database import get_db

router = APIRouter()

@router.get("/products", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Số trang"),
    size: int = Query(10, ge=1, le=100, description="Số sản phẩm mỗi trang"),
    category: Optional[str] = Query(None, description="Lọc theo danh mục"),
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of products (requires JWT authentication)
    
    - **page**: Số trang (bắt đầu từ 1)
    - **size**: Số sản phẩm mỗi trang (1-100)
    - **category**: Lọc theo danh mục (optional)
    - **search**: Tìm kiếm theo tên sản phẩm (optional)
    
    Yêu cầu: JWT token trong header Authorization
    - Header: `Authorization: Bearer <access_token>`
    
    Response:
    - **products**: Danh sách sản phẩm
    - **total**: Tổng số sản phẩm
    - **page**: Số trang hiện tại
    - **size**: Kích thước trang
    """
    # Query base - chỉ lấy sản phẩm active
    query = db.query(Product).filter(Product.is_active == True)
    
    # Lọc theo danh mục nếu có
    if category:
        query = query.filter(Product.category == category)
    
    # Tìm kiếm theo tên nếu có
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    # Tính tổng số sản phẩm
    total = query.count()
    
    # Phân trang
    offset = (page - 1) * size
    products = query.offset(offset).limit(size).all()
    
    return ProductListResponse(
        products=products,
        total=total,
        page=page,
        size=size
    )