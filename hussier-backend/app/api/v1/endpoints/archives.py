# app/api/endpoints/archives.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.crud.crud_archive import crud_archive
from app.schemas.archive import Archive, ArchiveCreate, ArchiveUpdate, ArchiveDetail
from app.models.archive import TypeArchive
from app.services import audit
from app.models.audit_log import ActionType, EntityType

router = APIRouter()


@router.get("", response_model=List[Archive])
def get_archives(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    """Récupérer toutes les archives"""
    archives = crud_archive.get_multi(db, skip=skip, limit=limit)
    return archives


@router.get("/{archive_id}", response_model=ArchiveDetail)
def get_archive(
    archive_id: int,
    db: Session = Depends(deps.get_db)
):
    """Récupérer une archive par ID"""
    archive = crud_archive.get(db, id=archive_id)
    if not archive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive non trouvée"
        )
    return archive


@router.get("/cabinet/{cabinet_id}", response_model=List[Archive])
def get_archives_by_cabinet(
    cabinet_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    """Récupérer les archives d'un cabinet"""
    archives = crud_archive.get_by_cabinet(
        db, cabinet_id=cabinet_id, skip=skip, limit=limit
    )
    return archives


@router.get("/type/{type_archive}", response_model=List[Archive])
def get_archives_by_type(
    type_archive: TypeArchive,
    cabinet_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    """Récupérer les archives par type"""
    archives = crud_archive.get_by_type(
        db, type_archive=type_archive, cabinet_id=cabinet_id, skip=skip, limit=limit
    )
    return archives


@router.get("/expires-soon/", response_model=List[Archive])
def get_archives_expires_soon(
    days: int = 30,
    cabinet_id: Optional[int] = None,
    db: Session = Depends(deps.get_db)
):
    """Récupérer les archives dont la suppression est proche"""
    archives = crud_archive.get_expires_soon(db, days=days, cabinet_id=cabinet_id)
    return archives


@router.post("", response_model=Archive, status_code=status.HTTP_201_CREATED)
def create_archive(
    archive_in: ArchiveCreate,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_user)
):
    """Créer une nouvelle archive"""
    existing = crud_archive.get_by_reference(
        db,
        type_archive=archive_in.type_archive,
        id_reference=archive_in.id_reference
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cette référence est déjà archivée"
        )

    archive = crud_archive.create(db, obj_in=archive_in)
    audit.record(db, current_user, request, action=ActionType.CREATE,
                 entity_type=EntityType.ARCHIVE, entity_id=archive.id,
                 description=f"Création de l'archive #{archive.id}")
    return archive


@router.put("/{archive_id}", response_model=Archive)
def update_archive(
    archive_id: int,
    archive_in: ArchiveUpdate,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_user)
):
    """Mettre à jour une archive"""
    archive = crud_archive.get(db, id=archive_id)
    if not archive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive non trouvée"
        )

    archive = crud_archive.update(db, db_obj=archive, obj_in=archive_in)
    audit.record(db, current_user, request, action=ActionType.UPDATE,
                 entity_type=EntityType.ARCHIVE, entity_id=archive_id,
                 description=f"Modification de l'archive #{archive_id}")
    return archive


@router.delete("/{archive_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_archive(
    archive_id: int,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_user)
):
    """Supprimer une archive définitivement"""
    archive = crud_archive.get(db, id=archive_id)
    if not archive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archive non trouvée"
        )

    crud_archive.delete(db, id=archive_id)
    audit.record(db, current_user, request, action=ActionType.DELETE,
                 entity_type=EntityType.ARCHIVE, entity_id=archive_id,
                 description=f"Suppression de l'archive #{archive_id}")
    return None
