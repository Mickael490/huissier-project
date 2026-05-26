# app/api/v1/endpoints/utilisateurs.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.crud import crud_utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate, UtilisateurInDB

router = APIRouter()

@router.post("", response_model=UtilisateurInDB, status_code=status.HTTP_201_CREATED)
def create_utilisateur(
    *,
    db: Session = Depends(deps.get_db),
    utilisateur_in: UtilisateurCreate
):
    """Créer un nouvel utilisateur"""
    if crud_utilisateur.get_by_email(db, email=utilisateur_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )
    return crud_utilisateur.create(db, obj_in=utilisateur_in)


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


@router.put("/{utilisateur_id}", response_model=UtilisateurInDB)
def update_utilisateur(
    *, db: Session = Depends(deps.get_db), utilisateur_id: int, utilisateur_in: UtilisateurUpdate
):
    db_obj = crud_utilisateur.get(db, id=utilisateur_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return crud_utilisateur.update(db, db_obj=db_obj, obj_in=utilisateur_in)


@router.delete("/{utilisateur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_utilisateur(*, db: Session = Depends(deps.get_db), utilisateur_id: int):
    utilisateur = crud_utilisateur.remove(db, id=utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return None