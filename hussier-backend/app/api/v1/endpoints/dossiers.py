from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.api import deps
from app.crud import crud_dossier
from app.schemas.dossier import DossierCreate, DossierUpdate, DossierResponse, DossierListResponse
from app.models.dossier import StatutDossier, TypeDossier

router = APIRouter()  # ✅ défini en premier

def generer_numero_dossier(db: Session) -> str:
    from app.models.dossier import Dossier as DossierModel
    annee = datetime.now().year
    # Cherche le max existant pour cette année et incrémente
    import re
    dossiers = db.query(DossierModel.numero_dossier).filter(
        DossierModel.numero_dossier.like(f"DOS-{annee}-%")
    ).all()
    if not dossiers:
        return f"DOS-{annee}-0001"
    numeros = []
    for (num,) in dossiers:
        match = re.search(r"DOS-\d{4}-(\d+)", num)
        if match:
            numeros.append(int(match.group(1)))
    next_num = max(numeros) + 1 if numeros else 1
    return f"DOS-{annee}-{next_num:04d}"

@router.get("", response_model=DossierListResponse)
def lister_dossiers(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    cabinet_id: Optional[int] = None,
    client_id: Optional[int] = None,
    statut: Optional[StatutDossier] = None,
    type_affaire: Optional[TypeDossier] = None,
) -> Any:
    dossiers = crud_dossier.get_multi(db, skip=skip, limit=limit)
    if cabinet_id:
        dossiers = [d for d in dossiers if d.cabinet_id == cabinet_id]
    if client_id:
        dossiers = [d for d in dossiers if d.client_id == client_id]
    if statut:
        dossiers = [d for d in dossiers if d.statut == statut]
    if type_affaire:
        dossiers = [d for d in dossiers if d.type_dossier == type_affaire]
    return {"total": len(dossiers), "skip": skip, "limit": limit, "dossiers": dossiers}

@router.post("", response_model=DossierResponse, status_code=201)
def creer_dossier(*, db: Session = Depends(deps.get_db), dossier_in: DossierCreate):
    if not dossier_in.numero_dossier:
        dossier_in.numero_dossier = generer_numero_dossier(db)
    # ✅ Calcul automatique du montant total
    principal = dossier_in.montant_principal or 0
    frais = dossier_in.montant_frais or 0
    dossier_in.montant_total = principal + frais
    return crud_dossier.create(db=db, obj_in=dossier_in)

@router.put("/{dossier_id}", response_model=DossierResponse)
def modifier_dossier(*, db: Session = Depends(deps.get_db), dossier_id: int, dossier_in: DossierUpdate):
    db_obj = crud_dossier.get(db=db, id=dossier_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    # ✅ Recalcul automatique du montant total
    principal = dossier_in.montant_principal if dossier_in.montant_principal is not None else (db_obj.montant_principal or 0)
    frais = dossier_in.montant_frais if dossier_in.montant_frais is not None else (db_obj.montant_frais or 0)
    dossier_in.montant_total = principal + frais
    return crud_dossier.update(db=db, db_obj=db_obj, obj_in=dossier_in)

@router.put("/{dossier_id}", response_model=DossierResponse)
def modifier_dossier(*, db: Session = Depends(deps.get_db), dossier_id: int, dossier_in: DossierUpdate):
    db_obj = crud_dossier.get(db=db, id=dossier_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    return crud_dossier.update(db=db, db_obj=db_obj, obj_in=dossier_in)

@router.delete("/{dossier_id}", status_code=204)
def supprimer_dossier(*, db: Session = Depends(deps.get_db), dossier_id: int):
    dossier = crud_dossier.remove(db=db, id=dossier_id)
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    return None

@router.post("/{dossier_id}/cloturer", response_model=DossierResponse)
def cloturer_dossier(*, db: Session = Depends(deps.get_db), dossier_id: int):
    dossier = crud_dossier.cloturer_dossier(db=db, dossier_id=dossier_id)
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    return dossier

@router.post("/{dossier_id}/archiver", response_model=DossierResponse)
def archiver_dossier(*, db: Session = Depends(deps.get_db), dossier_id: int):
    dossier = crud_dossier.archiver_dossier(db=db, dossier_id=dossier_id)
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    return dossier



@router.get("/stats/par-statut")
def statistiques_par_statut(db: Session = Depends(deps.get_db), cabinet_id: Optional[int] = None):
    return crud_dossier.compter_dossiers_par_statut(db=db, cabinet_id=cabinet_id)

@router.get("/stats/par-type")
def statistiques_par_type(db: Session = Depends(deps.get_db), cabinet_id: Optional[int] = None):
    return crud_dossier.compter_dossiers_par_type(db=db, cabinet_id=cabinet_id)