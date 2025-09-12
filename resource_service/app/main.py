"""
Resource Service - Entry point FastAPI
Xử lý resource (sản phẩm) với JWT authentication
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_products import router as products_router
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(
    title="Resource Service",
    description="Product Resource Service with JWT Authentication",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(products_router, prefix="/api", tags=["products"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Resource Service is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "resource_service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
