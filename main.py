from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine
from app.models import user, quran, hadith
from app.api.routes import quran, hadith, auth

# Create database tables
user.Base.metadata.create_all(bind=engine)
quran.Base.metadata.create_all(bind=engine)
hadith.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A comprehensive Quran and Hadith API backend"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(quran.router, prefix="/api/v1/quran", tags=["quran"])
app.include_router(hadith.router, prefix="/api/v1/hadith", tags=["hadith"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Quran Hadith API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
