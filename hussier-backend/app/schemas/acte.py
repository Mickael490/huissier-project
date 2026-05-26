# app/schemas/acte.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class TypeActeEnum(str, Enum):
    SIGNIFICATION = "signification"
    CONSTAT = "constat"
    SAISIE = "saisie"
    RECOUVREMENT = "recouvrement"
    EXPULSION = "expulsion"
    COMMANDEMENT = "commandement"
    PROCES_VERBAL = "proces_verbal"
    INVENTAIRE = "inventaire"
    AUTRE = "autre"


class ActeBase(BaseModel):
    """Schéma de base pour un acte"""
    type_acte: TypeActeEnum
    date_acte: date
    lieu: Optional[str] = None
    resultat: Optional[str] = None
    observations: Optional[str] = None


class ActeCreate(ActeBase):
    """Schéma pour créer un acte"""
    id_dossier: int = Field(..., gt=0)
    id_evenement: Optional[int] = Field(None, gt=0)


class ActeUpdate(BaseModel):
    """Schéma pour mettre à jour un acte"""
    type_acte: Optional[TypeActeEnum] = None
    date_acte: Optional[date] = None
    lieu: Optional[str] = None
    resultat: Optional[str] = None
    observations: Optional[str] = None
    id_evenement: Optional[int] = Field(None, gt=0)


class ActeInDB(ActeBase):
    """Schéma pour un acte en base de données"""
    id: int
    id_dossier: int
    id_evenement: Optional[int] = None

    class Config:
        from_attributes = True


class ActeResponse(ActeInDB):
    """Schéma de réponse API pour un acte"""
    pass
