# app/api/v1/endpoints/actes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.api import deps
from app.crud import crud_acte, crud_dossier
from app.schemas.acte import ActeCreate, ActeUpdate, ActeResponse

router = APIRouter()

@router.post("", response_model=ActeResponse, status_code=status.HTTP_201_CREATED)
def create_acte(*, db: Session = Depends(deps.get_db), acte_in: ActeCreate):
    """Créer un nouvel acte"""
    dossier = crud_dossier.get(db, id=acte_in.id_dossier)
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    # Créer dict avec type_acte en minuscule
    acte_data = acte_in.dict(exclude={'type_acte'})
    acte_data['type_acte'] = str(acte_in.type_acte).lower()
    # Créer objet Acte directement (sans schéma)
    from app.models.acte import Acte
    acte_obj = Acte(**acte_data)
    db.add(acte_obj)
    db.commit()
    db.refresh(acte_obj)
    return acte_obj

@router.get("", response_model=List[ActeResponse])
def read_actes(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    id_dossier: Optional[int] = Query(None, gt=0),
    type_acte: Optional[str] = None,
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None
):
    """Récupérer la liste des actes avec filtres optionnels"""
    return crud_acte.get_actes(
        db=db,
        skip=skip,
        limit=limit,
        id_dossier=id_dossier,
        type_acte=type_acte,
        date_debut=date_debut,
        date_fin=date_fin
    )

@router.get("/{acte_id}", response_model=ActeResponse)
def read_acte(*, db: Session = Depends(deps.get_db), acte_id: int):
    acte = crud_acte.get(db, id=acte_id)
    if not acte:
        raise HTTPException(status_code=404, detail="Acte non trouvé")
    return acte

@router.put("/{acte_id}", response_model=ActeResponse)
def update_acte(*, db: Session = Depends(deps.get_db), acte_id: int, acte_in: ActeUpdate):
    acte = crud_acte.get(db, id=acte_id)
    if not acte:
        raise HTTPException(status_code=404, detail="Acte non trouvé")
    return crud_acte.update(db, db_obj=acte, obj_in=acte_in)

@router.delete("/{acte_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_acte(*, db: Session = Depends(deps.get_db), acte_id: int):
    acte = crud_acte.get(db, id=acte_id)
    if not acte:
        raise HTTPException(status_code=404, detail="Acte non trouvé")
    crud_acte.remove(db, id=acte_id)