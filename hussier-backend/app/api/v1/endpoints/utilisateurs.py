# app/api/v1/endpoints/utilisateurs.py
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.crud import crud_utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate, UtilisateurInDB
from app.services import audit
from app.models.audit_log import ActionType, EntityType
from app.models.utilisateur import RoleEnum

router = APIRouter()

# Seul l'ADMIN gere les comptes ; la lecture est ouverte a tous les authentifies
ecriture_admin = Depends(deps.require_roles(RoleEnum.ADMIN))

@router.post("", response_model=UtilisateurInDB, status_code=status.HTTP_201_CREATED, dependencies=[ecriture_admin])
def create_utilisateur(
    *,
    db: Session = Depends(deps.get_db),
    utilisateur_in: UtilisateurCreate,
    request: Request,
    current_user=Depends(deps.get_current_active_user),
):
    """Créer un nouvel utilisateur"""
    if crud_utilisateur.get_by_email(db, email=utilisateur_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )
    utilisateur = crud_utilisateur.create(db, obj_in=utilisateur_in)
    audit.record(db, current_user, request, action=ActionType.CREATE,
                 entity_type=EntityType.UTILISATEUR, entity_id=utilisateur.id,
                 description=f"Création de l'utilisateur {utilisateur.email}")
    return utilisateur


@router.get("", response_model=List[UtilisateurInDB])
def read_utilisateurs(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    nom: Optional[str] = None,
    prenom: Optional[str] = None,
    email: Optional[str] = None,
    role: Optional[str] = None,
    actif: Optional[bool] = None
):
    """Récupérer la liste des utilisateurs avec filtres optionnels"""
    utilisateurs = crud_utilisateur.get_multi(db, skip=skip, limit=limit)
    filters = {k: v for k, v in {"nom": nom, "prenom": prenom, "email": email, "role": role, "actif": actif}.items() if v is not None}
    if filters:
        utilisateurs = [u for u in utilisateurs if all(getattr(u, k) == v for k, v in filters.items())]
    return utilisateurs


@router.get("/{utilisateur_id}", response_model=UtilisateurInDB)
def read_utilisateur(*, db: Session = Depends(deps.get_db), utilisateur_id: int):
    utilisateur = crud_utilisateur.get(db, id=utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return utilisateur


@router.put("/{utilisateur_id}", response_model=UtilisateurInDB, dependencies=[ecriture_admin])
def update_utilisateur(
    *, db: Session = Depends(deps.get_db), utilisateur_id: int, utilisateur_in: UtilisateurUpdate,
    request: Request, current_user=Depends(deps.get_current_active_user)
):
    db_obj = crud_utilisateur.get(db, id=utilisateur_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    utilisateur = crud_utilisateur.update(db, db_obj=db_obj, obj_in=utilisateur_in)
    audit.record(db, current_user, request, action=ActionType.UPDATE,
                 entity_type=EntityType.UTILISATEUR, entity_id=utilisateur_id,
                 description=f"Modification de l'utilisateur {utilisateur.email}")
    return utilisateur


@router.delete("/{utilisateur_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[ecriture_admin])
def delete_utilisateur(*, db: Session = Depends(deps.get_db), utilisateur_id: int,
                       request: Request, current_user=Depends(deps.get_current_active_user)):
    utilisateur = crud_utilisateur.remove(db, id=utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    audit.record(db, current_user, request, action=ActionType.DELETE,
                 entity_type=EntityType.UTILISATEUR, entity_id=utilisateur_id,
                 description=f"Suppression de l'utilisateur #{utilisateur_id}")
    return None