# app/models/utilisateur.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class RoleEnum(str, enum.Enum):
    """Rôles disponibles dans le système"""
    ADMIN = "admin"
    HUISSIER = "huissier"
    CLERC = "clerc"
    ASSISTANT = "assistant"
    SECRETAIRE = "secretaire"


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    # Identification
    id = Column(Integer, primary_key=True, index=True)
    id_cabinet = Column(Integer, ForeignKey("cabinets.id"), nullable=False, index=True)

    # Informations personnelles
    email = Column(String(255), unique=True, index=True, nullable=False)
    nom = Column(String(100), nullable=False, index=True)
    prenom = Column(String(100), nullable=False)
    telephone = Column(String(20))

    # Authentification
    mot_de_passe_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.SECRETAIRE)
    actif = Column(Boolean, default=True, nullable=False)

    # Métadonnées
    date_creation = Column(DateTime, default=func.now(), nullable=False)
    date_modification = Column(DateTime, default=func.now(), onupdate=func.now())
    derniere_connexion = Column(DateTime)

    # ===== RELATIONS =====
    cabinet = relationship("Cabinet", back_populates="utilisateurs")
    rendez_vous = relationship("Agenda", back_populates="utilisateur", cascade="all, delete-orphan")
    
    # Dossiers dont l'utilisateur est responsable
    dossiers_responsable = relationship(
        "Dossier",
        back_populates="utilisateur_responsable"
    )
    
    # Affectations où l'utilisateur est affecté à un dossier
    affectations = relationship(
        "AffectationDossier",
        back_populates="utilisateur",
        foreign_keys="[AffectationDossier.id_utilisateur]"
    )
    
    # Affectations que l'utilisateur a effectuées (qui a fait l'affectation)
    affectations_effectuees = relationship(
        "AffectationDossier",
        back_populates="affecte_par_utilisateur",
        foreign_keys="[AffectationDossier.affecte_par]"
    )

    def __repr__(self):
        return f"<Utilisateur(id={self.id}, email='{self.email}', nom='{self.nom}')>"
