# app/models/dossier.py
import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import func


from app.db.session import Base  # ← CORRECTION ICI


# ===== ENUMS =====
class StatutDossier(str, enum.Enum):
    """Statuts possibles d'un dossier"""
    NOUVEAU = "nouveau"
    EN_COURS = "en_cours"
    EN_ATTENTE = "en_attente"
    TERMINE = "termine"
    ARCHIVE = "archive"
    ANNULE = "annule"


class TypeDossier(str, enum.Enum):
    """Types de dossiers"""
    CONTENTIEUX = "contentieux"
    RECOUVREMENT = "recouvrement"
    CONSTAT = "constat"
    SIGNIFICATION = "signification"
    SAISIE = "saisie"
    EXPULSION = "expulsion"
    AUTRE = "autre"


# ===== MODÈLE DOSSIER =====
class Dossier(Base):
    """Table des dossiers"""
    
    __tablename__ = "dossiers"
    
    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)
    
    # Numéro de dossier (généré automatiquement)
    numero_dossier = Column(String(50), unique=True, nullable=False, index=True)
    
    # Informations principales
    objet = Column(String(255), nullable=False)
    description = Column(Text)
    type_dossier = Column(SQLEnum(TypeDossier), nullable=False)
    statut = Column(SQLEnum(StatutDossier), default=StatutDossier.NOUVEAU, nullable=False)
    mot_de_passe = Column(String(255), nullable=True)

    # Montants
    montant_principal = Column(Numeric(15, 2))
    montant_frais = Column(Numeric(15, 2))
    montant_total = Column(Numeric(15, 2))
    
    # Clés étrangères
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    cabinet_id = Column(Integer, ForeignKey("cabinets.id"), nullable=False)
    utilisateur_responsable_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=True, index=True) 
    
    # Dates
    date_ouverture = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_cloture = Column(DateTime)
    date_creation  = Column(DateTime, default=datetime.utcnow, nullable=False, server_default=func.now())
    date_modification  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, server_default=func.now())

    
    # Relations
    client = relationship("Client", back_populates="dossiers")
    cabinet = relationship("Cabinet", back_populates="dossiers")
    utilisateur_responsable = relationship("Utilisateur", back_populates="dossiers_responsable") 
    affectations = relationship("AffectationDossier", back_populates="dossier", cascade="all, delete-orphan")
    parties = relationship("Partie", back_populates="dossier", cascade="all, delete-orphan")
    actes = relationship("Acte", back_populates="dossier", cascade="all, delete-orphan")
    paiements = relationship("Paiement", back_populates="dossier", cascade="all, delete-orphan")
    evenements = relationship("Agenda", back_populates="dossier", cascade="all, delete-orphan")
    archive = relationship("Archive", back_populates="dossier", uselist=False, cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="dossier", cascade="all, delete-orphan")
    rendez_vous = relationship("Agenda", back_populates="dossier", cascade="all, delete-orphan")

    
    def __repr__(self):
         return f"<Partie(id={self.id}, nom={self.nom}, role={self.role})>"