# app/models/document.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, BigInteger
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime
import enum


class TypeDocument(str, enum.Enum):
    """Types de documents"""
    ACTE = "acte"                    # PV de signification, constat, etc.
    COURRIER = "courrier"            # Lettres, mails
    FACTURE = "facture"              # Factures émises/reçues
    PIECE_JOINTE = "piece_jointe"    # Documents annexes
    JUGEMENT = "jugement"            # Décisions de justice
    AUTRE = "autre"


class Document(Base):
    """Documents et fichiers liés aux dossiers"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    id_acte = Column(Integer, ForeignKey("actes.id"))  # Optionnel : si lié à un acte
    
    type_document = Column(SQLEnum(TypeDocument), nullable=False)
    nom_fichier = Column(String(255), nullable=False)         # "PV_Signification_2026.pdf"
    nom_original = Column(String(255), nullable=False)        # Nom donné par l'utilisateur
    chemin_fichier = Column(String(500), nullable=False)      # "/uploads/2026/02/abc123.pdf"
    
    mime_type = Column(String(100))                           # "application/pdf"
    taille_octets = Column(BigInteger)                        # Taille en bytes
    
    date_upload = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(String(500))                         # Description optionnelle

    # Relations
    dossier = relationship("Dossier", back_populates="documents")
    acte = relationship("Acte", back_populates="documents")

    def __repr__(self):
        return f"<Document(id={self.id}, nom={self.nom_fichier}, type={self.type_document})>"
