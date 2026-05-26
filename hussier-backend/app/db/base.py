# app/db/base.py
"""
Import tous les modèles SQLAlchemy existants
"""
from app.db.session import Base

# ✅ Importer TES 12 modèles (sans __init__.py)
from app.models.utilisateur import Utilisateur
from app.models.client import Client
from app.models.dossier import Dossier
from app.models.acte import Acte
from app.models.paiement import Paiement
from app.models.affectation_dossier import AffectationDossier
from app.models.partie import Partie
from app.models.agenda import Agenda
from app.models.archive import Archive
from app.models.audit_log import AuditLog
from app.models.statistic import Statistic
from app.models.cabinet import Cabinet

__all__ = ["Base"]
