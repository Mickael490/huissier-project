# app/models/agenda.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class TypeRendezVous(str, enum.Enum):
    """Types de rendez-vous"""
    SIGNIFICATION = "signification"
    CONSTAT = "constat"
    SAISIE = "saisie"
    AUDIENCE = "audience"
    CLIENT = "client"
    INTERNE = "interne"
    AUTRE = "autre"


class StatutRendezVous(str, enum.Enum):
    """Statuts de rendez-vous"""
    PLANIFIE = "planifie"
    CONFIRME = "confirme"
    EN_COURS = "en_cours"
    TERMINE = "termine"
    ANNULE = "annule"
    REPORTE = "reporte"


class PrioriteRendezVous(str, enum.Enum):
    """Priorités de rendez-vous"""
    BASSE = "basse"
    NORMALE = "normale"
    HAUTE = "haute"
    URGENTE = "urgente"


class Agenda(Base):
    """Modèle pour la gestion de l'agenda et des rendez-vous"""
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relations (notation SQL: id_xxx)
    id_dossier = Column(Integer, ForeignKey("dossiers.id", ondelete="SET NULL"), index=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False, index=True)
    id_client = Column(Integer, ForeignKey("clients.id", ondelete="SET NULL"), index=True)

    # Informations du rendez-vous
    titre = Column(String(200), nullable=False)
    type_rdv = Column(SQLEnum(TypeRendezVous), nullable=False, default=TypeRendezVous.AUTRE, index=True)
    statut = Column(SQLEnum(StatutRendezVous), nullable=False, default=StatutRendezVous.PLANIFIE, index=True)
    priorite = Column(SQLEnum(PrioriteRendezVous), nullable=False, default=PrioriteRendezVous.NORMALE)

    # Date et heure
    date_debut = Column(DateTime, nullable=False, index=True)
    date_fin = Column(DateTime, nullable=False)
    duree_minutes = Column(Integer, nullable=False, default=60)

    # Lieu
    lieu = Column(String(300))

    # Participants
    participants = Column(Text)

    # Rappels
    rappel_active = Column(Boolean, default=True)
    rappel_minutes_avant = Column(Integer, default=60)
    notification_envoyee = Column(Boolean, default=False)

    # Description
    description = Column(Text)
    notes_internes = Column(Text)

    # Annulation/Report
    annule = Column(Boolean, default=False)
    motif_annulation = Column(Text)
    date_annulation = Column(DateTime)
    reporte = Column(Boolean, default=False)
    ancienne_date = Column(DateTime)

    # Timestamps automatiques (harmonisation)
    date_creation = Column(DateTime, default=func.now(), nullable=False)
    date_modification = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    dossier = relationship("Dossier", back_populates="rendez_vous")
    utilisateur = relationship("Utilisateur", back_populates="rendez_vous")
    client = relationship("Client", back_populates="rendez_vous")
    acte = relationship("Acte", back_populates="evenement", uselist=False)

    def __repr__(self):
        return f"<Agenda(id={self.id}, reference={self.reference}, titre={self.titre})>"
