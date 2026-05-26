# app/schemas/cabinet.py
from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime


# ========== SCHÉMA DE BASE ==========
class CabinetBase(BaseModel):
    """Schéma de base pour Cabinet"""
    nom: str
    raison_sociale: Optional[str] = None
    adresse: str
    code_postal: Optional[str] = None
    ville: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    site_web: Optional[str] = None  
    logo_url: Optional[str] = None  
    numero_agrement: Optional[str] = None
    juridiction_rattachement: Optional[str] = None
    chambre_departementale: Optional[str] = None
    actif: bool = True


# ========== CRÉATION ==========
class CabinetCreate(CabinetBase):
    """Schéma pour créer un cabinet"""
    pass


# ========== MISE À JOUR ==========
class CabinetUpdate(BaseModel):
    """Schéma pour mettre à jour un cabinet (tous les champs optionnels)"""
    nom: Optional[str] = None
    raison_sociale: Optional[str] = None
    adresse: Optional[str] = None
    code_postal: Optional[str] = None
    ville: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    site_web: Optional[str] = None
    logo_url: Optional[str] = None
    numero_agrement: Optional[str] = None
    juridiction_rattachement: Optional[str] = None
    chambre_departementale: Optional[str] = None
    actif: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


# ========== LECTURE (RÉPONSE) ==========
class CabinetInDB(CabinetBase):
    """Schéma pour lire un cabinet (avec id et métadonnées)"""
    id: int
    date_creation: datetime
    date_modification: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Alias pour compatibilité
Cabinet = CabinetInDB


# ========== LISTE (PAGINATION) ==========
class CabinetList(BaseModel):
    """Schéma pour une liste de cabinets"""
    total: int
    items: list[CabinetInDB]

    model_config = ConfigDict(from_attributes=True)
