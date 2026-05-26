# app/models/acte.py
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class TypeActe(str, enum.Enum):
    SIGNIFICATION = "signification"
    CONSTAT = "constat"
    SAISIE = "saisie"
    RECOUVREMENT = "recouvrement"
    EXPULSION = "expulsion"
    COMMANDEMENT = "commandement"
    PROCES_VERBAL = "proces_verbal"
    INVENTAIRE = "inventaire"
    AUTRE = "autre"


class Acte(Base):
    """Actes et diligences"""
    __tablename__ = "actes"

    id = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    id_evenement = Column(Integer, ForeignKey("agenda.id"))
    
    type_acte = Column(SQLEnum(TypeActe), nullable=False)
    date_acte = Column(Date, nullable=False)
    lieu = Column(String)
    resultat = Column(Text)
    observations = Column(Text)

    # Relations
    dossier = relationship("Dossier", back_populates="actes")
    evenement = relationship("Agenda", back_populates="acte")
    documents = relationship("Document", back_populates="acte")


    def __repr__(self):
        return f"<Acte(id={self.id}, type={self.type_acte}, date={self.date_acte})>"
    
