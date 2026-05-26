# app/crud/crud_acte.py
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from app.models.acte import Acte
from app.schemas.acte import ActeCreate, ActeUpdate
from app.crud.crud_base import CRUDBase

class CRUDActe(CRUDBase[Acte, ActeCreate, ActeUpdate]):
    """CRUD spécifique pour les actes"""
    
    def get_actes(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        id_dossier: Optional[int] = None,
        type_acte: Optional[str] = None,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> List[Acte]:
        """Récupérer une liste d'actes avec filtres optionnels"""
        query = db.query(self.model)

        if id_dossier is not None:
            query = query.filter(Acte.id_dossier == id_dossier)
        
        if type_acte is not None:
            query = query.filter(Acte.type_acte == type_acte)
        
        if date_debut is not None:
            query = query.filter(Acte.date_acte >= date_debut)
        
        if date_fin is not None:
            query = query.filter(Acte.date_acte <= date_fin)

        return query.offset(skip).limit(limit).all()

# Instance globale
crud_acte = CRUDActe(Acte)