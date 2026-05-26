# app/schemas/agenda.py
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class TypeRendezVousEnum(str, Enum):
    """Types de rendez-vous"""
    SIGNIFICATION = "signification"
    CONSTAT = "constat"
    SAISIE = "saisie"
    AUDIENCE = "audience"
    CLIENT = "client"
    INTERNE = "interne"
    AUTRE = "autre"


class StatutRendezVousEnum(str, Enum):
    """Statuts de rendez-vous"""
    PLANIFIE = "planifie"
    CONFIRME = "confirme"
    EN_COURS = "en_cours"
    TERMINE = "termine"
    ANNULE = "annule"
    REPORTE = "reporte"


class PrioriteRendezVousEnum(str, Enum):
    """Priorités de rendez-vous"""
    BASSE = "basse"
    NORMALE = "normale"
    HAUTE = "haute"
    URGENTE = "urgente"


# ============================================================================
# SCHÉMAS DE BASE
# ============================================================================

class AgendaBase(BaseModel):
    """Schéma de base pour un rendez-vous"""
    titre: str = Field(..., min_length=1, max_length=200)
    type_rdv: TypeRendezVousEnum = TypeRendezVousEnum.AUTRE
    statut: StatutRendezVousEnum = StatutRendezVousEnum.PLANIFIE
    priorite: PrioriteRendezVousEnum = PrioriteRendezVousEnum.NORMALE
    date_debut: datetime
    date_fin: datetime
    duree_minutes: int = Field(60, ge=1)
    lieu: Optional[str] = Field(None, max_length=300)
    participants: Optional[str] = None
    description: Optional[str] = None
    notes_internes: Optional[str] = None
    rappel_active: bool = True
    rappel_minutes_avant: int = Field(60, ge=0)

    @field_validator('date_fin')
    @classmethod
    def validate_dates(cls, v, info):
        """Valider que date_fin > date_debut"""
        if 'date_debut' in info.data and v <= info.data['date_debut']:
            raise ValueError('La date de fin doit être après la date de début')
        return v


# ============================================================================
# CRÉATION
# ============================================================================

class AgendaCreate(AgendaBase):
    """Schéma pour créer un rendez-vous"""
    id_utilisateur: int = Field(..., gt=0)  # ✅ ALIGNÉ AVEC MODEL
    id_dossier: Optional[int] = Field(None, gt=0)  # ✅ ALIGNÉ AVEC MODEL
    id_client: Optional[int] = Field(None, gt=0)  # ✅ ALIGNÉ AVEC MODEL


# ============================================================================
# MISE À JOUR
# ============================================================================

class AgendaUpdate(BaseModel):
    """Schéma pour mettre à jour un rendez-vous"""
    titre: Optional[str] = Field(None, min_length=1, max_length=200)
    type_rdv: Optional[TypeRendezVousEnum] = None
    statut: Optional[StatutRendezVousEnum] = None
    priorite: Optional[PrioriteRendezVousEnum] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    duree_minutes: Optional[int] = Field(None, ge=1)
    lieu: Optional[str] = Field(None, max_length=300)
    participants: Optional[str] = None
    description: Optional[str] = None
    notes_internes: Optional[str] = None
    rappel_active: Optional[bool] = None
    rappel_minutes_avant: Optional[int] = Field(None, ge=0)
    annule: Optional[bool] = None
    motif_annulation: Optional[str] = None
    reporte: Optional[bool] = None


# ============================================================================
# LECTURE
# ============================================================================

class AgendaInDBBase(AgendaBase):
    """Schéma pour un rendez-vous en base de données"""
    id: int
    reference: str
    id_utilisateur: int  # ✅ ALIGNÉ AVEC MODEL
    id_dossier: Optional[int] = None  # ✅ ALIGNÉ AVEC MODEL
    id_client: Optional[int] = None  # ✅ ALIGNÉ AVEC MODEL
    notification_envoyee: bool
    annule: bool
    motif_annulation: Optional[str] = None
    date_annulation: Optional[datetime] = None
    reporte: bool
    ancienne_date: Optional[datetime] = None
    date_creation: datetime
    date_modification: datetime

    model_config = ConfigDict(from_attributes=True)


class Agenda(AgendaInDBBase):
    """Schéma complet d'un rendez-vous"""
    pass


class AgendaResponse(AgendaInDBBase):
    """Schéma de réponse API pour un rendez-vous"""
    pass
