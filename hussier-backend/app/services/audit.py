"""Service d'enregistrement des actions dans le journal d'audit.

Utilisation depuis un endpoint :

    from app.services import audit
    audit.record(
        db, current_user, request,
        action=ActionType.CREATE,
        entity_type=EntityType.CLIENT,
        entity_id=client.id,
        description=f"Création du client {client.nom}",
    )

Le log est volontairement « best-effort » : si l'écriture échoue, on
n'interrompt jamais l'opération métier (rollback local + log silencieux).
"""
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from fastapi import Request

from app.models.audit_log import AuditLog, ActionType, EntityType


def record(
    db: Session,
    current_user=None,
    request: Optional[Request] = None,
    *,
    action: ActionType,
    entity_type: EntityType,
    entity_id: Optional[int] = None,
    description: Optional[str] = None,
    donnees_avant: Optional[Dict[str, Any]] = None,
    donnees_apres: Optional[Dict[str, Any]] = None,
) -> None:
    """Enregistre une entrée d'audit. Best-effort : n'échoue jamais."""
    try:
        log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            donnees_avant=donnees_avant,
            donnees_apres=donnees_apres,
            id_utilisateur=getattr(current_user, "id", None),
            id_cabinet=getattr(current_user, "id_cabinet", None),
            ip_address=_client_ip(request),
            user_agent=(request.headers.get("user-agent") if request else None),
        )
        db.add(log)
        db.commit()
    except Exception:
        # L'audit ne doit jamais casser l'opération métier.
        db.rollback()


def _client_ip(request: Optional[Request]) -> Optional[str]:
    if request is None:
        return None
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None
