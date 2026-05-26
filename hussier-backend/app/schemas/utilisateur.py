# app/schemas/utilisateur.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UtilisateurBase(BaseModel):
    """Schéma de base pour un utilisateur"""
    email: EmailStr
    nom: str
    prenom: str
    telephone: Optional[str] = None
    role: str = "utilisateur"  # admin, huissier, assistant, utilisateur
    actif: bool = True


class UtilisateurCreate(UtilisateurBase):
    id_cabinet: int = 1
    """Schéma pour créer un utilisateur"""
    mot_de_passe: str = Field(..., min_length=8, description="Mot de passe (minimum 8 caractères)")


class UtilisateurUpdate(BaseModel):
    """Schéma pour mettre à jour un utilisateur"""
    email: Optional[EmailStr] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    telephone: Optional[str] = None
    role: Optional[str] = None
    actif: Optional[bool] = None
    mot_de_passe: Optional[str] = Field(None, min_length=8)


class UtilisateurInDB(UtilisateurBase):
    """Schéma pour un utilisateur en base de données (réponse API)"""
    id: int
    date_creation: datetime
    date_modification: datetime
    derniere_connexion: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permet la conversion depuis SQLAlchemy
