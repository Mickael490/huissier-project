from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Request
from app.api import deps
from app.crud import crud_dossier
from app.schemas.dossier import DossierCreate, DossierUpdate, DossierResponse, DossierListResponse
from app.models.dossier import StatutDossier, TypeDossier
from app.services import audit
from app.models.audit_log import ActionType, EntityType
from app.services.email import envoyer_email, template_changement_statut
from app.models.client import Client

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
def creer_dossier(*, db: Session = Depends(deps.get_db), dossier_in: DossierCreate,
                  request: Request, current_user=Depends(deps.get_current_active_user)):
    if not dossier_in.numero_dossier:
        dossier_in.numero_dossier = generer_numero_dossier(db)
    # ✅ Calcul automatique du montant total
    principal = dossier_in.montant_principal or 0
    frais = dossier_in.montant_frais or 0
    dossier_in.montant_total = principal + frais
    dossier = crud_dossier.create(db=db, obj_in=dossier_in)
    audit.record(db, current_user, request, action=ActionType.CREATE,
                 entity_type=EntityType.DOSSIER, entity_id=dossier.id,
                 description=f"Création du dossier {dossier.numero_dossier}")
    return dossier

@router.put("/{dossier_id}", response_model=DossierResponse)
def modifier_dossier(*, db: Session = Depends(deps.get_db), dossier_id: int, dossier_in: DossierUpdate,
                     request: Request, current_user=Depends(deps.get_current_active_user)):
    db_obj = crud_dossier.get(db=db, id=dossier_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    # ✅ Recalcul automatique du montant total
    principal = dossier_in.montant_principal if dossier_in.montant_principal is not None else (db_obj.montant_principal or 0)
    frais = dossier_in.montant_frais if dossier_in.montant_frais is not None else (db_obj.montant_frais or 0)
    dossier_in.montant_total = principal + frais

    # ✅ Notification email si le statut change
    ancien_statut = db_obj.statut
    nouveau_statut = dossier_in.statut if dossier_in.statut is not None else ancien_statut

    dossier = crud_dossier.update(db=db, db_obj=db_obj, obj_in=dossier_in)

    if nouveau_statut and ancien_statut and nouveau_statut != ancien_statut and dossier.client_id:
        client = db.query(Client).filter(Client.id == dossier.client_id).first()
        if client and client.email:
            try:
                corps = template_changement_statut(
                    numero_dossier=dossier.numero_dossier,
                    objet=dossier.objet or "",
                    ancien_statut=ancien_statut.value if hasattr(ancien_statut, "value") else str(ancien_statut),
                    nouveau_statut=nouveau_statut.value if hasattr(nouveau_statut, "value") else str(nouveau_statut)
                )
                envoyer_email(
                    destinataire=client.email,
                    sujet=f"Mise a jour de votre dossier {dossier.numero_dossier}",
                    corps_html=corps
                )
            except Exception:
                pass  # Ne jamais bloquer la requete si l'email echoue

    audit.record(db, current_user, request, action=ActionType.UPDATE,
                 entity_type=EntityType.DOSSIER, entity_id=dossier_id,
                 description=f"Modification du dossier {dossier.numero_dossier}")
    return dossier

@router.delete("/{dossier_id}", status_code=204)
def supprimer_dossier(*, db: Session = Depends(deps.get_db), dossier_id: int,
                      request: Request, current_user=Depends(deps.get_current_active_user)):
    dossier = crud_dossier.remove(db=db, id=dossier_id)
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    audit.record(db, current_user, request, action=ActionType.DELETE,
                 entity_type=EntityType.DOSSIER, entity_id=dossier_id,
                 description=f"Suppression du dossier #{dossier_id}")
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