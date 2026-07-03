from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud.crud_audit_log import crud_audit_log
from app.schemas.audit_log import AuditLog
from app.models.audit_log import AuditLog as AuditLogModel, ActionType

router = APIRouter()

# Journal d'audit : lecture seule. La création se fait côté serveur
# (app/services/audit.py), jamais via l'API. Aucune suppression possible
# pour garantir l'intégrité de la traçabilité. Routeur restreint ADMIN
# au niveau de app/api/v1/api.py.

@router.get("/", response_model=List[AuditLog])
def get_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_audit_log.get_multi(db, skip=skip, limit=limit)

@router.get("/stats")
def get_audit_stats(db: Session = Depends(deps.get_db)):
    """Statistiques globales du journal d'audit (KPI)."""
    return {
        "total": db.query(AuditLogModel).count(),
        "creations": db.query(AuditLogModel).filter(AuditLogModel.action == ActionType.CREATE).count(),
        "modifications": db.query(AuditLogModel).filter(AuditLogModel.action == ActionType.UPDATE).count(),
        "suppressions": db.query(AuditLogModel).filter(AuditLogModel.action == ActionType.DELETE).count(),
    }

@router.get("/{log_id}", response_model=AuditLog)
def get_audit_log(log_id: int, db: Session = Depends(deps.get_db)):
    log = crud_audit_log.get(db, id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log non trouvé")
    return log

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_log(log_id: int, db: Session = Depends(deps.get_db)):
    # Réservé ADMIN (routeur restreint dans app/api/v1/api.py).
    log = crud_audit_log.get(db, id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log non trouvé")
    crud_audit_log.delete(db, id=log_id)
    return None
