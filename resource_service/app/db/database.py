"""
Database configuration and session management
Session + init data cho Resource Service
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True  # Verify connections before use
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with tables and seed data"""
    # Create data directory if it doesn't exist
    data_dir = os.path.dirname(settings.DATABASE_URL.replace("sqlite:///./", ""))
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    
    create_tables()
    seed_data()

def create_tables():
    """Create all tables"""
    from app.models.product import Base
    Base.metadata.create_all(bind=engine)

def seed_data():
    """Seed initial product data"""
    from app.models.product import Product
    
    db = SessionLocal()
    try:
        # Check if products exist
        product_count = db.query(Product).count()
        if product_count == 0:
            sample_products = [
                Product(
                    name="Laptop Gaming",
                    description="Laptop gaming cao cấp với card đồ họa RTX 4060",
                    price=25000000,
                    category="Electronics",
                    stock_quantity=10
                ),
                Product(
                    name="iPhone 15 Pro",
                    description="iPhone 15 Pro với chip A17 Pro",
                    price=30000000,
                    category="Electronics",
                    stock_quantity=5
                ),
                Product(
                    name="Nike Air Max",
                    description="Giày thể thao Nike Air Max",
                    price=2500000,
                    category="Fashion",
                    stock_quantity=20
                ),
                Product(
                    name="MacBook Pro M3",
                    description="MacBook Pro với chip M3 mới nhất",
                    price=45000000,
                    category="Electronics",
                    stock_quantity=3
                )
            ]
            
            for product in sample_products:
                db.add(product)
            
            db.commit()
            print("Sample products created")
    finally:
        db.close()
