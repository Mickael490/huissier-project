# app/api/endpoints/agendas.py
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.api import deps
from app.crud.crud_agenda import crud_agenda
from app.crud.crud_utilisateur import crud_utilisateur
from app.crud.crud_dossier import crud_dossier
from app.crud.crud_client import crud_client
from app.services import audit
from app.models.audit_log import ActionType, EntityType
from app.services.email import envoyer_email, template_nouveau_rendezvous
import threading
from app.schemas.agenda import (
    AgendaCreate,
    AgendaUpdate,
    AgendaResponse,
    TypeRendezVousEnum,
    StatutRendezVousEnum
)

router = APIRouter()


@router.post("", response_model=AgendaResponse, status_code=status.HTTP_201_CREATED)
def create_agenda(
    *,
    db: Session = Depends(deps.get_db),
    request: Request,
    current_user=Depends(deps.get_current_active_user),
    agenda_in: AgendaCreate
):
    """Créer un nouveau rendez-vous"""
    # Vérifier que l'utilisateur existe
    utilisateur = crud_utilisateur.get(db, id=agenda_in.id_utilisateur)
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )

    # Vérifier le dossier si fourni
    if agenda_in.id_dossier:
        dossier = crud_dossier.get(db, id=agenda_in.id_dossier)
        if not dossier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dossier non trouvé"
            )

    # Vérifier le client si fourni
    if agenda_in.id_client:
        client = crud_client.get(db, id=agenda_in.id_client)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client non trouvé"
            )

    # Créer l'agenda
    agenda = crud_agenda.create(db, obj_in=agenda_in)

    # Notification email au client (en arriere-plan, ne bloque jamais la reponse)
    try:
        if agenda.id_client:
            client = crud_client.get(db, id=agenda.id_client)
            if client and client.email:
                corps = template_nouveau_rendezvous(
                    titre=agenda.titre,
                    date_debut=agenda.date_debut.strftime("%d/%m/%Y a %H:%M"),
                    lieu=agenda.lieu or "",
                    type_rdv=agenda.type_rdv.value if hasattr(agenda.type_rdv, "value") else str(agenda.type_rdv)
                )
                threading.Thread(
                    target=envoyer_email,
                    args=(client.email, f"Rendez-vous planifie - {agenda.titre}", corps),
                    daemon=True
                ).start()
    except Exception:
        pass  # Ne jamais bloquer la requete si l'email echoue

    audit.record(db, current_user, request, action=ActionType.CREATE,
                 entity_type=EntityType.AGENDA, entity_id=agenda.id,
                 description=f"Création du rendez-vous #{agenda.id}")
    return agenda


@router.get("", response_model=List[AgendaResponse])
def read_agendas(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    utilisateur_id: Optional[int] = Query(None, gt=0),
    dossier_id: Optional[int] = Query(None, gt=0),
    client_id: Optional[int] = Query(None, gt=0),
    type_rdv: Optional[TypeRendezVousEnum] = None,
    statut: Optional[StatutRendezVousEnum] = None,
    date_debut_min: Optional[datetime] = None,
    date_fin_max: Optional[datetime] = None
):
    """Récupérer la liste des rendez-vous avec filtres optionnels"""
    from app.models.agenda import Agenda
    
    query = db.query(Agenda)
    
    if utilisateur_id:
        query = query.filter(Agenda.id_utilisateur == utilisateur_id)
    
    if dossier_id:
        query = query.filter(Agenda.id_dossier == dossier_id)
    
    if client_id:
        query = query.filter(Agenda.id_client == client_id)
    
    if type_rdv:
        query = query.filter(Agenda.type_rdv == type_rdv.value)
    
    if statut:
        query = query.filter(Agenda.statut == statut.value)
    
    if date_debut_min:
        query = query.filter(Agenda.date_debut >= date_debut_min)
    
    if date_fin_max:
        query = query.filter(Agenda.date_fin <= date_fin_max)
    
    agendas = query.order_by(Agenda.date_debut).offset(skip).limit(limit).all()
    return agendas


@router.get("/{agenda_id}", response_model=AgendaResponse)
def read_agenda(
    *,
    db: Session = Depends(deps.get_db),
    agenda_id: int
):
    """Récupérer un rendez-vous par son ID"""
    agenda = crud_agenda.get(db, id=agenda_id)
    if not agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rendez-vous non trouvé"
        )
    return agenda


@router.put("/{agenda_id}", response_model=AgendaResponse)
def update_agenda(
    *,
    db: Session = Depends(deps.get_db),
    request: Request,
    current_user=Depends(deps.get_current_active_user),
    agenda_id: int,
    agenda_in: AgendaUpdate
):
    """Mettre à jour un rendez-vous"""
    db_agenda = crud_agenda.get(db, id=agenda_id)
    if not db_agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rendez-vous non trouvé"
        )

    agenda = crud_agenda.update(db, db_obj=db_agenda, obj_in=agenda_in)
    audit.record(db, current_user, request, action=ActionType.UPDATE,
                 entity_type=EntityType.AGENDA, entity_id=agenda_id,
                 description=f"Modification du rendez-vous #{agenda_id}")
    return agenda


@router.delete("/{agenda_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agenda(
    *,
    db: Session = Depends(deps.get_db),
    request: Request,
    current_user=Depends(deps.get_current_active_user),
    agenda_id: int
):
    """Supprimer un rendez-vous"""
    db_agenda = crud_agenda.get(db, id=agenda_id)
    if not db_agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rendez-vous non trouvé"
        )

    crud_agenda.remove(db, id=agenda_id)
    audit.record(db, current_user, request, action=ActionType.DELETE,
                 entity_type=EntityType.AGENDA, entity_id=agenda_id,
                 description=f"Suppression du rendez-vous #{agenda_id}")
    return None


@router.post("/{agenda_id}/annuler", response_model=AgendaResponse)
def annuler_agenda(
    *,
    db: Session = Depends(deps.get_db),
    agenda_id: int,
    motif: str = Query(..., min_length=1)
):
    """Annuler un rendez-vous"""
    db_agenda = crud_agenda.get(db, id=agenda_id)
    if not db_agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rendez-vous non trouvé"
        )
    
    if db_agenda.annule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rendez-vous déjà annulé"
        )
    
    agenda = crud_agenda.annuler(db, db_obj=db_agenda, motif=motif)
    return agenda


@router.post("/{agenda_id}/reporter", response_model=AgendaResponse)
def reporter_agenda(
    *,
    db: Session = Depends(deps.get_db),
    agenda_id: int,
    nouvelle_date_debut: datetime,
    nouvelle_date_fin: datetime
):
    """Reporter un rendez-vous"""
    db_agenda = crud_agenda.get(db, id=agenda_id)
    if not db_agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rendez-vous non trouvé"
        )
    
    if nouvelle_date_fin <= nouvelle_date_debut:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nouvelle date de fin doit être après la date de début"
        )
    
    agenda = crud_agenda.reporter(
        db,
        db_obj=db_agenda,
        nouvelle_date_debut=nouvelle_date_debut,
        nouvelle_date_fin=nouvelle_date_fin
    )
    return agenda
