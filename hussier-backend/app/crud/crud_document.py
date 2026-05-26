# app/crud/crud_document.py
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.document import Document, TypeDocument
from app.schemas.document import DocumentCreate, DocumentUpdate
import os
from datetime import datetime
import uuid


class CRUDDocument:
    """CRUD pour les documents"""

    def get_document(self, db: Session, document_id: int) -> Optional[Document]:
        """Récupérer un document par ID"""
        return db.query(Document).filter(Document.id == document_id).first()

    def get_documents_by_dossier(
        self, 
        db: Session, 
        dossier_id: int,
        type_document: Optional[TypeDocument] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Document]:
        """Récupérer tous les documents d'un dossier"""
        query = db.query(Document).filter(Document.id_dossier == dossier_id)

        if type_document:
            query = query.filter(Document.type_document == type_document)

        return query.offset(skip).limit(limit).all()

    def count_documents_by_dossier(
        self,
        db: Session,
        dossier_id: int,
        type_document: Optional[TypeDocument] = None
    ) -> int:
        """Compter les documents d'un dossier"""
        query = db.query(Document).filter(Document.id_dossier == dossier_id)

        if type_document:
            query = query.filter(Document.type_document == type_document)

        return query.count()

    # 👇 NOUVELLES MÉTHODES AJOUTÉES
    def get_all_documents(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        type_document: Optional[str] = None
    ) -> List[Document]:
        """Récupérer tous les documents avec filtres optionnels"""
        query = db.query(Document)
        
        if type_document:
            query = query.filter(Document.type_document == type_document)
        
        return query.order_by(Document.date_upload.desc()).offset(skip).limit(limit).all()

    def count_all_documents(
        self,
        db: Session,
        type_document: Optional[str] = None
    ) -> int:
        """Compter tous les documents"""
        query = db.query(Document)
        
        if type_document:
            query = query.filter(Document.type_document == type_document)
        
        return query.count()
    # 👆 FIN DES NOUVELLES MÉTHODES

    def create_document_metadata(
        self,
        db: Session,
        *,
        document_in: DocumentCreate,
        nom_fichier: str,
        nom_original: str,
        chemin_fichier: str,
        mime_type: str,
        taille_octets: int
    ) -> Document:
        """Créer les métadonnées d'un document"""
        db_document = Document(
            id_dossier=document_in.id_dossier,
            id_acte=document_in.id_acte,
            type_document=document_in.type_document,
            nom_fichier=nom_fichier,
            nom_original=nom_original,
            chemin_fichier=chemin_fichier,
            mime_type=mime_type,
            taille_octets=taille_octets,
            description=document_in.description
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document

    def update_document(
        self,
        db: Session,
        *,
        document_id: int,
        document_update: DocumentUpdate
    ) -> Optional[Document]:
        """Mettre à jour un document (métadonnées uniquement)"""
        db_document = self.get_document(db, document_id)
        if not db_document:
            return None

        update_data = document_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_document, field, value)

        db.commit()
        db.refresh(db_document)
        return db_document

    def delete_document(self, db: Session, document_id: int) -> bool:
        """Supprimer un document (fichier + métadonnées)"""
        db_document = self.get_document(db, document_id)
        if not db_document:
            return False

        # Supprimer le fichier physique
        try:
            if os.path.exists(db_document.chemin_fichier):
                os.remove(db_document.chemin_fichier)
        except Exception as e:
            print(f"Erreur suppression fichier: {e}")

        # Supprimer les métadonnées
        db.delete(db_document)
        db.commit()
        return True

    def generate_filename(self, original_filename: str) -> str:
        """Générer un nom de fichier unique"""
        extension = os.path.splitext(original_filename)[1]
        unique_id = uuid.uuid4().hex[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{unique_id}{extension}"

    def generate_filepath(self, filename: str, base_dir: str = "uploads") -> str:
        """Générer le chemin complet du fichier"""
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")
        directory = os.path.join(base_dir, year, month)

        # Créer les répertoires si nécessaire
        os.makedirs(directory, exist_ok=True)

        return os.path.join(directory, filename)


# Instance singleton
crud_document = CRUDDocument()
