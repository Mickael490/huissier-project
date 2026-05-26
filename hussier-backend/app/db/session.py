from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Créer le moteur SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Affiche les requêtes SQL (à mettre False en production)
)

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Dependency pour FastAPI
def get_db():
    """
    Générateur de session de base de données
    À utiliser comme dépendance dans les routes FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
