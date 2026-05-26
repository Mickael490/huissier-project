# app/schemas/affectation_dossier.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


# Schéma de base
class AffectationDossierBase(BaseModel):
    id_dossier: int
    id_utilisateur: int
    commentaire: Optional[str] = None


# Schéma pour la création
class AffectationDossierCreate(AffectationDossierBase):
    affecte_par: int


# Schéma pour la mise à jour
class AffectationDossierUpdate(BaseModel):
    commentaire: Optional[str] = None
    date_fin: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Schéma pour la lecture
class AffectationDossier(AffectationDossierBase):
    id: int
    affecte_par: int
    date_affectation: datetime
    date_fin: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Schéma détaillé avec relations
class AffectationDossierDetail(AffectationDossier):
    dossier: Optional[dict] = None
    utilisateur: Optional[dict] = None
    affecteur: Optional[dict] = None


# Schéma pour la réaffectation
class AffectationDossierReassign(BaseModel):
    id_dossier: int
    new_utilisateur_id: int
    commentaire: Optional[str] = None
