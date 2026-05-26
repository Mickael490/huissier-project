# app/models/client.py
from sqlalchemy import Column, Integer, String, Text, Date, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class TypeClient(str, enum.Enum):
    PARTICULIER = "particulier"
    AVOCAT = "avocat"
    ENTREPRISE = "entreprise"
    JURIDICTION = "juridiction"


class Client(Base):
    """Modèle Client"""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    id_cabinet = Column(Integer, ForeignKey("cabinets.id"), nullable=False)
    
    type_client = Column(SQLEnum(TypeClient), nullable=False, index=True)
    nom = Column(String, nullable=False, index=True)
    prenom = Column(String)
    adresse = Column(Text)
    telephone = Column(String)
    email = Column(String, index=True)
    siret = Column(String(14))
    representant_legal = Column(String)
    mot_de_passe = Column(String, nullable=True)
    
    # Timestamps automatiques
    date_creation = Column(DateTime, default=func.now(), nullable=False)
    date_modification = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    cabinet = relationship("Cabinet", back_populates="clients")
    dossiers = relationship("Dossier", back_populates="client")
    rendez_vous = relationship("Agenda", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client(id={self.id}, nom={self.nom}, type={self.type_client})>"

