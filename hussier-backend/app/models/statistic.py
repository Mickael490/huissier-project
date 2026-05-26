# app/models/statistic.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import date
import enum

from app.db.session import Base  # ✅ CORRIGÉ


class TypeStatistique(str, enum.Enum):
    CABINET = "CABINET"
    DOSSIER = "DOSSIER"
    FINANCIER = "FINANCIER"
    UTILISATEUR = "UTILISATEUR"
    ACTIVITE = "ACTIVITE"


class PeriodeStatistique(str, enum.Enum):
    JOUR = "JOUR"
    SEMAINE = "SEMAINE"
    MOIS = "MOIS"
    TRIMESTRE = "TRIMESTRE"
    ANNEE = "ANNEE"


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    id_cabinet = Column(Integer, ForeignKey("cabinets.id"), nullable=False)
    type_statistique = Column(Enum(TypeStatistique), nullable=False)
    periode = Column(Enum(PeriodeStatistique), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    nom_metrique = Column(String(100), nullable=False)
    valeur_numerique = Column(Float)
    valeur_texte = Column(String(500))
    details_json = Column(String)
    calcule_le = Column(Date, default=date.today)

    # Relations
    cabinet = relationship("Cabinet", back_populates="statistics")
