# app/core/config.py
import os
import secrets
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional, Union

class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "Huissier App"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:3000",
        "http://localhost:5173",
        "https://lighthearted-monstera-5aaf13.netlify.app",
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/dossier_db"
    
    # Security
    # En production, definir SECRET_KEY dans .env. Sinon une cle aleatoire est
    # generee au demarrage (les sessions ne survivent pas a un redemarrage).
    SECRET_KEY: str = secrets.token_urlsafe(64)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # Alias pour compatibilité
    
    # Email (optionnel)
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: str = "noreply@huissier-system.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    
    # Redis (optionnel)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        # Permet de definir BACKEND_CORS_ORIGINS dans .env en liste separee par virgules
        # ex: BACKEND_CORS_ORIGINS=https://app.mondomaine.com,https://www.mondomaine.com
        if isinstance(v, str) and not v.startswith("["):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"  # ✅ Ignore les champs extra du .env

settings = Settings()
