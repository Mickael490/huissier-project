# app/crud/__init__.py
from app.crud.crud_cabinet import crud_cabinet
from app.crud.crud_client import crud_client
from app.crud.crud_utilisateur import crud_utilisateur
from app.crud.crud_dossier import crud_dossier
from app.crud.crud_acte import crud_acte
from app.crud.crud_partie import crud_partie
from app.crud.crud_document import crud_document
from app.crud.crud_agenda import crud_agenda           
from app.crud.crud_archive import crud_archive
from app.crud.crud_audit_log import crud_audit_log
from app.crud.crud_affectation_dossier import crud_affectation_dossier
from app.crud.crud_statistic import crud_statistic


__all__ = [
    "crud_cabinet",
    "crud_client",
    "crud_utilisateur",
    "crud_dossier",
    "crud_partie",
    "crud_agenda",
    "crud_acte",
    "crud_document",
    "crud_archive",
    "crud_audit_log",
    "crud_affectation_dossier",
    "crud_statistic"
]
