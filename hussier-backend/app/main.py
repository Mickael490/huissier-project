from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router  # ← AJOUTER CETTE LIGNE

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    redirect_slashes=False
)

# Configuration CORS (origines definies dans app/core/config.py ou via .env)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Inclure les routes API
app.include_router(api_router, prefix=settings.API_V1_STR)

# Routes principales
@app.get("/")
async def root():
    return {
        "message": f"{settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs": "/docs",
        "api": settings.API_V1_STR
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
