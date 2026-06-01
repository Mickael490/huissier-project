# app/models/paiement.py
from sqlalchemy import Column, Integer, Numeric, Date, Boolean, ForeignKey, Enum as SQLEnum, String
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class TypePaiement(str, enum.Enum):
    FRAIS = "frais"
    AVANCE = "avance"
    RECOUVREMENT = "recouvrement"


class ModePaiement(str, enum.Enum):
    ESPECES = "especes"
    CHEQUE = "cheque"
    VIREMENT = "virement"


class Paiement(Base):
    """Paiements liés aux dossiers"""
    __tablename__ = "paiements"

    id = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    
    type_paiement = Column(String, nullable=False)
    montant = Column(Numeric(10, 2), nullable=False)
    date_paiement = Column(Date, nullable=False)
    mode_paiement = Column(String, nullable=False)
    reverse_au_client = Column(Boolean, default=False)
    mot_de_passe = Column(String, nullable=True)
    numero_cheque = Column(String, nullable=True)
    reference_virement = Column(String, nullable=True)
    reseau_mobile = Column(String, nullable=True)
    numero_mobile = Column(String, nullable=True)
    autre_mode = Column(String, nullable=True)

    # Relations
    dossier = relationship("Dossier", back_populates="paiements")

    def __repr__(self):
        return f"<Paiement(id={self.id_paiement}, montant={self.montant}, type={self.type_paiement})>"
