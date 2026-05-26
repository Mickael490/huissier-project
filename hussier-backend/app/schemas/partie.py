# app/schemas/partie.py
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class RolePartieEnum(str, Enum):
    """Rôles possibles pour une partie"""
    DEBITEUR = "debiteur"
    DESTINATAIRE = "destinataire"
    AUTRE = "autre"


class PartieBase(BaseModel):
    """Schéma de base pour une partie"""
    nom: str = Field(..., min_length=1, max_length=200)
    role: RolePartieEnum
    adresse: Optional[str] = None
    contact: Optional[str] = None


class PartieCreate(PartieBase):
    """Schéma pour créer une partie"""
    id_dossier: int = Field(..., gt=0)


class PartieUpdate(BaseModel):
    """Schéma pour mettre à jour une partie"""
    nom: Optional[str] = Field(None, min_length=1, max_length=200)
    role: Optional[RolePartieEnum] = None
    adresse: Optional[str] = None
    contact: Optional[str] = None


class PartieInDB(PartieBase):
    """Schéma pour une partie en base de données"""
    id: int
    id_dossier: int

    class Config:
        from_attributes = True


class PartieResponse(PartieInDB):
    """Schéma de réponse API"""
    pass
