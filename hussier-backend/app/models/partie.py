# app/models/partie.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class RolePartie(str, enum.Enum):
    DEBITEUR = "debiteur"
    DESTINATAIRE = "destinataire"
    AUTRE = "autre"


class Partie(Base):
    """Parties impliquées dans un dossier"""
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    
    nom = Column(String, nullable=False)
    role = Column(SQLEnum(RolePartie), nullable=False)
    adresse = Column(Text)
    contact = Column(String)

    # Relations
    dossier = relationship("Dossier", back_populates="parties")

    def __repr__(self):
        return f"<Partie(id={self.id_partie}, nom={self.nom}, role={self.role})>"
