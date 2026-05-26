from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.crud import crud_partie, crud_dossier
from app.schemas.partie import PartieCreate, PartieUpdate, PartieResponse

router = APIRouter()

@router.post("", response_model=PartieResponse, status_code=status.HTTP_201_CREATED)
def create_partie(*, db: Session = Depends(deps.get_db), partie_in: PartieCreate):
    dossier = crud_dossier.get(db, id=partie_in.id_dossier)
    if not dossier:
        raise HTTPException(status_code=404, detail=f"Dossier {partie_in.id_dossier} non trouvé")
    return crud_partie.create(db=db, obj_in=partie_in)

@router.get("", response_model=List[PartieResponse])
def read_parties(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    id_dossier: Optional[int] = Query(None)
):
    if id_dossier is not None:
        return crud_partie.get_by_dossier(db, id_dossier=id_dossier, skip=skip, limit=limit)
    return crud_partie.get_multi(db, skip=skip, limit=limit)

@router.get("/{partie_id}", response_model=PartieResponse)
def read_partie(*, db: Session = Depends(deps.get_db), partie_id: int):
    partie = crud_partie.get(db, id=partie_id)
    if not partie:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    return partie

@router.put("/{partie_id}", response_model=PartieResponse)
def update_partie(*, db: Session = Depends(deps.get_db), partie_id: int, partie_in: PartieUpdate):
    db_partie = crud_partie.get(db, id=partie_id)
    if not db_partie:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    return crud_partie.update(db, db_obj=db_partie, obj_in=partie_in)

@router.delete("/{partie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partie(*, db: Session = Depends(deps.get_db), partie_id: int):
    partie = crud_partie.remove(db, id=partie_id)
    if not partie:
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    return None
