# app/models/cabinet.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Cabinet(Base):
    """
    Modèle Cabinet d'huissier
    Paramètres et informations du cabinet
    """
    __tablename__ = "cabinets"

    id = Column(Integer, primary_key=True, index=True)

    # Informations principales
    nom = Column(String, nullable=False, index=True)
    raison_sociale = Column(String)

    # Coordonnées
    adresse = Column(Text, nullable=False)
    code_postal = Column(String)
    ville = Column(String)
    telephone = Column(String)
    email = Column(String, index=True)
    site_web = Column(String)

    # Identité visuelle
    logo_url = Column(String)
    
    numero_agrement = Column(String, unique=True)
    juridiction_rattachement = Column(String)
    chambre_departementale = Column(String)

   
    # Métadonnées
    actif = Column(Boolean, default=True)
    date_creation = Column(DateTime, default=func.now())
    date_modification = Column(DateTime, onupdate=func.now())

    # RELATIONS OBLIGATOIRES
    utilisateurs = relationship("Utilisateur", back_populates="cabinet")
    clients = relationship("Client", back_populates="cabinet")
    dossiers = relationship("Dossier", back_populates="cabinet")
    statistics = relationship("Statistic", back_populates="cabinet")
    
    def __repr__(self):
        return f"<Cabinet(id={self.id}, nom='{self.nom}')>"
