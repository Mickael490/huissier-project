# app/models/audit_log.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.session import Base 


class ActionType(str, enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    VIEW = "VIEW"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXPORT = "EXPORT"
    PRINT = "PRINT"


class EntityType(str, enum.Enum):
    CABINET = "CABINET"
    CLIENT = "CLIENT"
    DOSSIER = "DOSSIER"
    ACTE = "ACTE"
    PARTIE = "PARTIE"
    DOCUMENT = "DOCUMENT"
    PAIEMENT = "PAIEMENT"
    UTILISATEUR = "UTILISATEUR"
    ARCHIVE = "ARCHIVE"
    AGENDA = "AGENDA"
    AFFECTATION = "AFFECTATION"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id"))
    id_cabinet = Column(Integer, ForeignKey("cabinets.id"))
    action = Column(Enum(ActionType), nullable=False)
    entity_type = Column(Enum(EntityType), nullable=False)
    entity_id = Column(Integer)
    description = Column(Text)
    donnees_avant = Column(JSON)
    donnees_apres = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    date_action = Column(DateTime, default=datetime.utcnow, index=True)

    # Relations
    utilisateur = relationship("Utilisateur")
