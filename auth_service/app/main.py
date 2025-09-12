"""
Auth Service - Entry point FastAPI
Xử lý authentication và authorization với RSA JWT
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_auth import router as auth_router
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(
    title="Authentication Service",
    description="RSA JWT Authentication Service",
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
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Auth Service is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth_service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
