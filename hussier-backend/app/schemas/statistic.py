# app/schemas/statistic.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import date, datetime


# Schéma de base
class StatisticBase(BaseModel):
    type_statistique: str
    periode: str
    id_cabinet: int
    date_debut: date
    date_fin: date
    nom_metrique: str
    valeur_numerique: Optional[float] = None
    valeur_texte: Optional[str] = None
    details_json: Optional[str] = None  # ⚠️ String car SQLAlchemy String(max)


# Schéma pour la création
class StatisticCreate(StatisticBase):
    pass


# Schéma pour la mise à jour
class StatisticUpdate(BaseModel):
    valeur_numerique: Optional[float] = None
    valeur_texte: Optional[str] = None
    details_json: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Schéma pour la lecture
class Statistic(StatisticBase):
    id: int
    calcule_le: date

    model_config = ConfigDict(from_attributes=True)


# Schémas pour les endpoints spéciaux
class DashboardStats(BaseModel):
    dossiers: Dict[str, int]
    clients: Dict[str, int]
    utilisateurs: Dict[str, int]

    model_config = ConfigDict(from_attributes=True)


class TendancesStats(BaseModel):
    periode_jours: int
    nouveaux_dossiers: int
    dossiers_clos: int

    model_config = ConfigDict(from_attributes=True)
