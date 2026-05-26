# app/schemas/document.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum


class TypeDocumentEnum(str, Enum):
    """Types de documents"""
    ACTE = "acte"
    COURRIER = "courrier"
    FACTURE = "facture"
    PIECE_JOINTE = "piece_jointe"
    JUGEMENT = "jugement"
    AUTRE = "autre"


class DocumentBase(BaseModel):
    """Schéma de base d'un document"""
    type_document: TypeDocumentEnum
    id_acte: Optional[int] = None
    description: Optional[str] = Field(None, max_length=500)


class DocumentCreate(DocumentBase):
    """Schéma pour créer un document (utilisé avec upload)"""
    id_dossier: int


class DocumentUpdate(BaseModel):
    """Schéma pour mettre à jour un document"""
    type_document: Optional[TypeDocumentEnum] = None
    description: Optional[str] = Field(None, max_length=500)
    id_acte: Optional[int] = None


class DocumentInDB(DocumentBase):
    """Schéma document en base"""
    id: int
    id_dossier: int
    nom_fichier: str
    nom_original: str
    chemin_fichier: str
    mime_type: Optional[str]
    taille_octets: Optional[int]
    date_upload: datetime

    class Config:
        from_attributes = True


class DocumentResponse(DocumentInDB):
    """Schéma de réponse API"""
    taille_lisible: str = ""  # "2.5 MB"
    url_telechargement: str = ""  # "/api/v1/documents/123/download"

    @validator('taille_lisible', always=True)
    def calculer_taille_lisible(cls, v, values):
        """Convertir les octets en format lisible"""
        taille = values.get('taille_octets', 0)
        if not taille:
            return "0 B"
        
        for unite in ['B', 'KB', 'MB', 'GB']:
            if taille < 1024.0:
                return f"{taille:.1f} {unite}"
            taille /= 1024.0
        return f"{taille:.1f} TB"

    @validator('url_telechargement', always=True)
    def generer_url(cls, v, values):
        """Générer l'URL de téléchargement"""
        doc_id = values.get('id')
        return f"/api/v1/documents/{doc_id}/download" if doc_id else ""


class DocumentList(BaseModel):
    """Liste paginée de documents"""
    total: int
    documents: list[DocumentResponse]
