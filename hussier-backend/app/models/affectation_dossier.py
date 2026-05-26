from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, Boolean, String, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class AffectationDossier(Base):
    __tablename__ = "affectations_dossier"

    id = Column(Integer, primary_key=True, index=True)
    id_dossier = Column(Integer, ForeignKey("dossiers.id"), nullable=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id"), nullable=True)
    affecte_par = Column(Integer, ForeignKey("utilisateurs.id"), nullable=True)

    # Nouveaux champs
    id_acte = Column(Integer, ForeignKey("actes.id"), nullable=True)
    agent_nom = Column(String(200))
    agent_role = Column(String(100))
    date_affectation = Column(DateTime, default=datetime.utcnow)
    date_limite = Column(Date, nullable=True)
    priorite = Column(String(20), default='normale')
    statut = Column(String(30), default='en_cours')
    instructions = Column(Text)
    notes = Column(Text)
    est_actif = Column(Boolean, default=True)

    # Relations
    dossier = relationship("Dossier", back_populates="affectations")
    utilisateur = relationship("Utilisateur", foreign_keys=[id_utilisateur])
    affecte_par_utilisateur = relationship("Utilisateur", foreign_keys=[affecte_par])