from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.paiement import Paiement
from app.schemas.paiement import PaiementCreate, PaiementUpdate, PaiementResponse

router = APIRouter()

@router.get("", response_model=List[PaiementResponse])
def get_paiements(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    return db.query(Paiement).offset(skip).limit(limit).all()

@router.post("", response_model=PaiementResponse, status_code=201)
def create_paiement(*, db: Session = Depends(deps.get_db), paiement_in: PaiementCreate):
    paiement = Paiement(**paiement_in.model_dump())
    db.add(paiement)
    db.commit()
    db.refresh(paiement)
    return paiement

@router.get("/{paiement_id}", response_model=PaiementResponse)
def get_paiement(*, db: Session = Depends(deps.get_db), paiement_id: int):
    paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement non trouvé")
    return paiement

@router.put("/{paiement_id}", response_model=PaiementResponse)
def update_paiement(*, db: Session = Depends(deps.get_db), paiement_id: int, paiement_in: PaiementUpdate):
    paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement non trouvé")
    for field, value in paiement_in.model_dump(exclude_unset=True).items():
        setattr(paiement, field, value)
    db.commit()
    db.refresh(paiement)
    return paiement

@router.delete("/{paiement_id}", status_code=204)
def delete_paiement(*, db: Session = Depends(deps.get_db), paiement_id: int):
    paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement non trouvé")
    db.delete(paiement)
    db.commit()
    return None
