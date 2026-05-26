# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional

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
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/dossier_db"
    
    # Security
    SECRET_KEY: str = "votre-cle-secrete-super-longue-et-aleatoire-changez-moi"
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
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"  # ✅ Ignore les champs extra du .env

settings = Settings()
