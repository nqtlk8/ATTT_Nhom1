"""
Pydantic schemas for Product Service
Product schemas và response models
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    """Base product schema"""
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock_quantity: int = 0

class ProductCreate(ProductBase):
    """Product creation schema"""
    pass


class ProductResponse(ProductBase):
    """Product response schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    """Product list response schema"""
    products: List[ProductResponse]
    total: int
    page: int
    size: int

class UserInfo(BaseModel):
    """User info from JWT token"""
    user_id: int
    username: str
    is_admin: bool = False
