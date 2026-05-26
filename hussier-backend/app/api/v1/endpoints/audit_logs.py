from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud.crud_audit_log import crud_audit_log
from app.schemas.audit_log import AuditLog, AuditLogCreate, AuditLogDetail

router = APIRouter()

@router.get("/", response_model=List[AuditLog])
def get_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_audit_log.get_multi(db, skip=skip, limit=limit)

@router.get("/{log_id}", response_model=AuditLog)
def get_audit_log(log_id: int, db: Session = Depends(deps.get_db)):
    log = crud_audit_log.get(db, id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log non trouvé")
    return log

@router.post("/", response_model=AuditLog, status_code=status.HTTP_201_CREATED)
def create_audit_log(log_in: AuditLogCreate, db: Session = Depends(deps.get_db)):
    return crud_audit_log.create(db, obj_in=log_in)

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_log(log_id: int, db: Session = Depends(deps.get_db)):
    log = crud_audit_log.get(db, id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log non trouvé")
    crud_audit_log.delete(db, id=log_id)
    return None
