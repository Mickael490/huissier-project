from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.crud import crud_client
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.services import audit
from app.models.audit_log import ActionType, EntityType
from app.models.utilisateur import RoleEnum

router = APIRouter()

# Roles autorises a modifier les clients (la lecture est ouverte a tous les authentifies)
ecriture_clients = Depends(deps.require_roles(RoleEnum.ADMIN, RoleEnum.HUISSIER, RoleEnum.CLERC, RoleEnum.SECRETAIRE))

@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED, dependencies=[ecriture_clients])
def create_client(*, db: Session = Depends(deps.get_db), client_in: ClientCreate,
                  request: Request, current_user=Depends(deps.get_current_active_user)):
    if client_in.email:
        existing = crud_client.get_by_email(db, email=client_in.email)
        if existing:
            raise HTTPException(status_code=400, detail="Un client avec cet email existe déjà")
    client = crud_client.create(db, obj_in=client_in)
    audit.record(db, current_user, request, action=ActionType.CREATE,
                 entity_type=EntityType.CLIENT, entity_id=client.id,
                 description=f"Création du client #{client.id}")
    return client

@router.get("", response_model=List[ClientResponse])
def read_clients(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    cabinet_id: Optional[int] = Query(None, gt=0),
    type_client: Optional[str] = None
):
    return crud_client.get_multi(db, skip=skip, limit=limit, cabinet_id=cabinet_id, type_client=type_client)

@router.get("/{client_id}", response_model=ClientResponse)
def read_client(*, db: Session = Depends(deps.get_db), client_id: int):
    client = crud_client.get(db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@router.put("/{client_id}", response_model=ClientResponse, dependencies=[ecriture_clients])
def update_client(*, db: Session = Depends(deps.get_db), client_id: int, client_in: ClientUpdate,
                  request: Request, current_user=Depends(deps.get_current_active_user)):
    db_obj = crud_client.get(db, id=client_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    client = crud_client.update(db, db_obj=db_obj, obj_in=client_in)
    audit.record(db, current_user, request, action=ActionType.UPDATE,
                 entity_type=EntityType.CLIENT, entity_id=client_id,
                 description=f"Modification du client #{client_id}")
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[ecriture_clients])
def delete_client(*, db: Session = Depends(deps.get_db), client_id: int,
                  request: Request, current_user=Depends(deps.get_current_active_user)):
    client = crud_client.delete(db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    audit.record(db, current_user, request, action=ActionType.DELETE,
                 entity_type=EntityType.CLIENT, entity_id=client_id,
                 description=f"Suppression du client #{client_id}")
    return None
