from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.paiement import Paiement
from app.schemas.paiement import PaiementCreate, PaiementUpdate, PaiementResponse
from app.services import audit
from app.models.audit_log import ActionType, EntityType
from app.services.email import envoyer_email, template_paiement_recu
import threading
from app.models.dossier import Dossier
from app.models.client import Client

router = APIRouter()

@router.get("", response_model=List[PaiementResponse])
def get_paiements(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    return db.query(Paiement).offset(skip).limit(limit).all()

@router.post("", response_model=PaiementResponse, status_code=201)
def create_paiement(*, db: Session = Depends(deps.get_db), paiement_in: PaiementCreate,
                    request: Request, current_user=Depends(deps.get_current_active_user)):
    data = paiement_in.model_dump()
    if data.get('type_paiement'):
        data['type_paiement'] = data['type_paiement'].lower()
    if data.get('mode_paiement'):
        data['mode_paiement'] = data['mode_paiement'].lower()
    paiement = Paiement(**data)
    db.add(paiement)
    db.commit()
    db.refresh(paiement)

    # Notification email au client (en arriere-plan, ne bloque jamais la reponse)
    try:
        dossier = db.query(Dossier).filter(Dossier.id == paiement.id_dossier).first()
        if dossier and dossier.client_id:
            client = db.query(Client).filter(Client.id == dossier.client_id).first()
            if client and client.email:
                corps = template_paiement_recu(
                    numero_dossier=dossier.numero_dossier,
                    montant=float(paiement.montant),
                    type_paiement=paiement.type_paiement
                )
                threading.Thread(
                    target=envoyer_email,
                    args=(client.email, f"Confirmation de paiement - Dossier {dossier.numero_dossier}", corps),
                    daemon=True
                ).start()
    except Exception:
        pass  # Ne jamais bloquer la requete si l'email echoue

    audit.record(db, current_user, request, action=ActionType.CREATE,
                 entity_type=EntityType.PAIEMENT, entity_id=paiement.id,
                 description=f"Enregistrement du paiement #{paiement.id}")
    return paiement

@router.get("/{paiement_id}", response_model=PaiementResponse)
def get_paiement(*, db: Session = Depends(deps.get_db), paiement_id: int):
    paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement non trouvé")
    return paiement

@router.put("/{paiement_id}", response_model=PaiementResponse)
def update_paiement(*, db: Session = Depends(deps.get_db), paiement_id: int, paiement_in: PaiementUpdate,
                    request: Request, current_user=Depends(deps.get_current_active_user)):
    paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement non trouvé")
    data = paiement_in.model_dump(exclude_unset=True)
    if data.get('type_paiement'):
        data['type_paiement'] = data['type_paiement'].lower()
    if data.get('mode_paiement'):
        data['mode_paiement'] = data['mode_paiement'].lower()
    for field, value in data.items():
        setattr(paiement, field, value)
    db.commit()
    db.refresh(paiement)
    audit.record(db, current_user, request, action=ActionType.UPDATE,
                 entity_type=EntityType.PAIEMENT, entity_id=paiement_id,
                 description=f"Modification du paiement #{paiement_id}")
    return paiement

@router.delete("/{paiement_id}", status_code=204)
def delete_paiement(*, db: Session = Depends(deps.get_db), paiement_id: int,
                    request: Request, current_user=Depends(deps.get_current_active_user)):
    paiement = db.query(Paiement).filter(Paiement.id == paiement_id).first()
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement non trouvé")
    db.delete(paiement)
    db.commit()
    audit.record(db, current_user, request, action=ActionType.DELETE,
                 entity_type=EntityType.PAIEMENT, entity_id=paiement_id,
                 description=f"Suppression du paiement #{paiement_id}")
    return None
