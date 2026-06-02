from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
import os

from app.api import deps
from app.crud.crud_document import crud_document
from app.crud.crud_dossier import crud_dossier
from app.schemas.document import DocumentResponse, DocumentList, DocumentUpdate, TypeDocumentEnum, DocumentCreate
from app.services import audit
from app.models.audit_log import ActionType, EntityType

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_MIME_TYPES = [
    "application/pdf", "image/jpeg", "image/png", "image/jpg",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
]

@router.get("", response_model=DocumentList)
def get_all_documents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    type_document: Optional[TypeDocumentEnum] = None
):
    documents = crud_document.get_all_documents(db, skip=skip, limit=limit, type_document=type_document)
    total = crud_document.count_all_documents(db, type_document=type_document)
    return {"total": total, "documents": documents}

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    *,
    db: Session = Depends(deps.get_db),
    request: Request,
    current_user=Depends(deps.get_current_active_user),
    file: UploadFile = File(...),
    id_dossier: int = Form(...),
    type_document: TypeDocumentEnum = Form(...),
    id_acte: Optional[int] = Form(None),
    description: Optional[str] = Form(None)
):
    dossier = crud_dossier.get(db, id=id_dossier)
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé")

    contents = await file.read()
    file_size = len(contents)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux. Maximum: 10 MB")

    filename = crud_document.generate_filename(file.filename)
    filepath = crud_document.generate_filepath(filename)

    try:
        with open(filepath, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur sauvegarde: {str(e)}")

    document_in = DocumentCreate(
        id_dossier=id_dossier,
        type_document=type_document,
        id_acte=id_acte,
        description=description
    )

    document = crud_document.create_document_metadata(
        db,
        document_in=document_in,
        nom_fichier=filename,
        nom_original=file.filename,
        chemin_fichier=filepath,
        mime_type=file.content_type,
        taille_octets=file_size
    )

    audit.record(db, current_user, request, action=ActionType.CREATE,
                 entity_type=EntityType.DOCUMENT, entity_id=document.id,
                 description=f"Ajout du document {file.filename}")
    return document

@router.get("/dossier/{dossier_id}", response_model=DocumentList)
def get_documents_by_dossier(
    *, db: Session = Depends(deps.get_db), dossier_id: int,
    type_document: Optional[TypeDocumentEnum] = None, skip: int = 0, limit: int = 100
):
    documents = crud_document.get_documents_by_dossier(db, dossier_id=dossier_id, type_document=type_document, skip=skip, limit=limit)
    total = crud_document.count_documents_by_dossier(db, dossier_id=dossier_id, type_document=type_document)
    return {"total": total, "documents": documents}

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(*, db: Session = Depends(deps.get_db), document_id: int):
    document = crud_document.get_document(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    return document

@router.get("/{document_id}/download")
def download_document(*, db: Session = Depends(deps.get_db), document_id: int):
    document = crud_document.get_document(db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    if not os.path.exists(document.chemin_fichier):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    return FileResponse(path=document.chemin_fichier, filename=document.nom_original, media_type=document.mime_type)

@router.patch("/{document_id}", response_model=DocumentResponse)
def update_document(*, db: Session = Depends(deps.get_db), document_id: int, document_in: DocumentUpdate,
                    request: Request, current_user=Depends(deps.get_current_active_user)):
    document = crud_document.update_document(db, document_id=document_id, document_update=document_in)
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    audit.record(db, current_user, request, action=ActionType.UPDATE,
                 entity_type=EntityType.DOCUMENT, entity_id=document_id,
                 description=f"Modification du document #{document_id}")
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(*, db: Session = Depends(deps.get_db), document_id: int,
                    request: Request, current_user=Depends(deps.get_current_active_user)):
    success = crud_document.delete_document(db, document_id=document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    audit.record(db, current_user, request, action=ActionType.DELETE,
                 entity_type=EntityType.DOCUMENT, entity_id=document_id,
                 description=f"Suppression du document #{document_id}")
    return None
