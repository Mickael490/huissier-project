# app/models/__init__.py
from app.db.session import Base
from app.models.cabinet import Cabinet
from app.models.client import Client, TypeClient
from app.models.utilisateur import Utilisateur, RoleEnum
from app.models.dossier import Dossier, TypeDossier, StatutDossier
from app.models.affectation_dossier import AffectationDossier
from app.models.partie import Partie, RolePartie
from app.models.agenda import Agenda, TypeRendezVous, StatutRendezVous, PrioriteRendezVous
from app.models.acte import Acte, TypeActe
from app.models.paiement import Paiement
from app.models.archive import Archive, TypeArchive
from app.models.audit_log import AuditLog
from app.models.document import Document
from app.models.statistic import Statistic

__all__ = [
    "Base",
    "Cabinet",        
    "Client",
    "TypeClient",
    "Utilisateur",
    "RoleEnum",
    "Dossier",
    "TypeDossier",
    "StatutDossier",
    "AffectationDossier",
    "Partie",
    "RolePartie",
    "Agenda",
    "TypeEvenement",
    "StatutEvenement",
    "Acte",
    "TypeActe",
    "Paiement",
    "Archive",
    "TypeArchive",
    "AuditLog",   
    "Agenda",
    "TypeRendezVous",
    "StatutRendezVous",
    "PrioriteRendezVous", 
    "Document",
    "Statistic"
]
