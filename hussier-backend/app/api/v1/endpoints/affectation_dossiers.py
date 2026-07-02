from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from pydantic import BaseModel
from app.api import deps
from app.models.affectation_dossier import AffectationDossier
from app.services import audit
from app.models.audit_log import ActionType, EntityType
from app.services.email import envoyer_email, template_nouvelle_affectation
from app.models.utilisateur import Utilisateur
from app.models.dossier import Dossier
import threading

router = APIRouter()

class AffectationIn(BaseModel):
    id_dossier: Optional[int] = None
    id_acte: Optional[int] = None
    id_utilisateur: Optional[int] = None
    affecte_par: Optional[int] = None
    agent_nom: Optional[str] = None
    agent_role: Optional[str] = None
    date_limite: Optional[str] = None
    priorite: Optional[str] = "normale"
    statut: Optional[str] = "en_cours"
    instructions: Optional[str] = None
    notes: Optional[str] = None

@router.get("", response_model=List[dict])
def get_affectations(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    affectations = db.query(AffectationDossier).offset(skip).limit(limit).all()
    return [
        {
            "id": a.id,
            "id_dossier": a.id_dossier,
            "id_acte": a.id_acte,
            "id_utilisateur": a.id_utilisateur,
            "affecte_par": a.affecte_par,
            "agent_nom": a.agent_nom,
            "agent_role": a.agent_role,
            "date_affectation": str(a.date_affectation) if a.date_affectation else None,
            "date_limite": str(a.date_limite) if a.date_limite else None,
            "priorite": a.priorite,
            "statut": a.statut,
            "instructions": a.instructions,
            "notes": a.notes,
            "est_actif": a.est_actif,
        }
        for a in affectations
    ]

@router.post("", status_code=201)
def create_affectation(affectation_in: AffectationIn, request: Request,
                       db: Session = Depends(deps.get_db),
                       current_user=Depends(deps.get_current_active_user)):
    affectation = AffectationDossier(
        id_dossier=affectation_in.id_dossier,
        id_acte=affectation_in.id_acte,
        id_utilisateur=affectation_in.id_utilisateur,
        affecte_par=affectation_in.affecte_par or affectation_in.id_utilisateur,
        agent_nom=affectation_in.agent_nom,
        agent_role=affectation_in.agent_role,
        date_limite=affectation_in.date_limite,
        priorite=affectation_in.priorite or "normale",
        statut=affectation_in.statut or "en_cours",
        instructions=affectation_in.instructions,
        notes=affectation_in.notes,
        est_actif=True
    )
    db.add(affectation)
    db.commit()
    db.refresh(affectation)

    # Notification email a l'agent affecte (en arriere-plan, ne bloque jamais la reponse)
    try:
        if affectation.id_utilisateur:
            agent = db.query(Utilisateur).filter(Utilisateur.id == affectation.id_utilisateur).first()
            if agent and agent.email:
                dossier = db.query(Dossier).filter(Dossier.id == affectation.id_dossier).first() if affectation.id_dossier else None
                corps = template_nouvelle_affectation(
                    numero_dossier=dossier.numero_dossier if dossier else "N/A",
                    objet=dossier.objet if dossier else "",
                    priorite=affectation.priorite or "normale",
                    date_limite=str(affectation.date_limite) if affectation.date_limite else "",
                    instructions=affectation.instructions or ""
                )
                threading.Thread(
                    target=envoyer_email,
                    args=(agent.email, f"Nouvelle mission affectee - Dossier {dossier.numero_dossier if dossier else affectation.id}", corps),
                    daemon=True
                ).start()
    except Exception:
        pass  # Ne jamais bloquer la requete si l'email echoue

    audit.record(db, current_user, request, action=ActionType.CREATE,
                 entity_type=EntityType.AFFECTATION, entity_id=affectation.id,
                 description=f"Création de l'affectation #{affectation.id}")
    return {"id": affectation.id, "message": "Affectation créée avec succès"}

@router.put("/{affectation_id}", status_code=200)
def update_affectation(affectation_id: int, affectation_in: AffectationIn, request: Request,
                       db: Session = Depends(deps.get_db),
                       current_user=Depends(deps.get_current_active_user)):
    affectation = db.query(AffectationDossier).filter(AffectationDossier.id == affectation_id).first()
    if not affectation:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    for key, value in affectation_in.model_dump(exclude_none=True).items():
        if hasattr(affectation, key):
            setattr(affectation, key, value)
    db.commit()
    db.refresh(affectation)
    audit.record(db, current_user, request, action=ActionType.UPDATE,
                 entity_type=EntityType.AFFECTATION, entity_id=affectation_id,
                 description=f"Modification de l'affectation #{affectation_id}")
    return {"id": affectation.id, "message": "Affectation mise à jour"}

@router.delete("/{affectation_id}", status_code=204)
def delete_affectation(affectation_id: int, request: Request,
                       db: Session = Depends(deps.get_db),
                       current_user=Depends(deps.get_current_active_user)):
    affectation = db.query(AffectationDossier).filter(
        AffectationDossier.id == affectation_id
    ).first()

    if not affectation:
        return None

    db.delete(affectation)
    db.commit()

    audit.record(db, current_user, request, action=ActionType.DELETE,
                 entity_type=EntityType.AFFECTATION, entity_id=affectation_id,
                 description=f"Suppression de l'affectation #{affectation_id}")
    return None

