# app/models/archive.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.session import Base 


class TypeArchive(str, enum.Enum):
    DOSSIER = "DOSSIER"
    ACTE = "ACTE"
    DOCUMENT = "DOCUMENT"
    PAIEMENT = "PAIEMENT"


class Archive(Base):
    __tablename__ = "archives"

    id = Column(Integer, primary_key=True, index=True)
    dossier_id = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    type_archive = Column(Enum(TypeArchive), nullable=False)
    id_reference = Column(Integer, nullable=False)
    id_cabinet = Column(Integer, ForeignKey("cabinets.id"), nullable=False)
    donnees_json = Column(Text, nullable=False)
    raison_archivage = Column(Text)
    mot_de_passe = Column(String, nullable=True)
    archive_par = Column(Integer, ForeignKey("utilisateurs.id"))
    date_archivage = Column(DateTime, default=datetime.utcnow)
    date_suppression_prevue = Column(DateTime)

    # Relations
    utilisateur = relationship("Utilisateur")
    dossier = relationship("Dossier", back_populates="archive")
