# app/api/v1/endpoints/cabinets.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_cabinet
from app.schemas.cabinet import CabinetCreate, CabinetUpdate, CabinetInDB
from app.models.utilisateur import RoleEnum

router = APIRouter()

ecriture_admin = Depends(deps.require_roles(RoleEnum.ADMIN))

@router.get("", response_model=List[CabinetInDB])
def list_cabinets(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_cabinet.get_multi(db, skip=skip, limit=limit)

@router.get("/{cabinet_id}", response_model=CabinetInDB)
def get_cabinet(cabinet_id: int, db: Session = Depends(deps.get_db)):
    db_cabinet = crud_cabinet.get(db, id=cabinet_id)
    if not db_cabinet:
        raise HTTPException(status_code=404, detail="Cabinet non trouvé")
    return db_cabinet

@router.post("", response_model=CabinetInDB, status_code=status.HTTP_201_CREATED, dependencies=[ecriture_admin])
def create_cabinet(cabinet_in: CabinetCreate, db: Session = Depends(deps.get_db)):
    try:
        return crud_cabinet.create(db, obj_in=cabinet_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{cabinet_id}", response_model=CabinetInDB, dependencies=[ecriture_admin])
def update_cabinet(cabinet_id: int, cabinet_in: CabinetUpdate, db: Session = Depends(deps.get_db)):
    db_cabinet = crud_cabinet.get(db, id=cabinet_id)
    if not db_cabinet:
        raise HTTPException(status_code=404, detail="Cabinet non trouvé")
    return crud_cabinet.update(db, db_obj=db_cabinet, obj_in=cabinet_in)

@router.delete("/{cabinet_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[ecriture_admin])
def delete_cabinet(cabinet_id: int, db: Session = Depends(deps.get_db)):
    db_cabinet = crud_cabinet.get(db, id=cabinet_id)
    if not db_cabinet:
        raise HTTPException(status_code=404, detail="Cabinet non trouvé")
    crud_cabinet.remove(db, id=cabinet_id)