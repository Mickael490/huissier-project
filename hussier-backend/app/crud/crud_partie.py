# app/crud/crud_partie.py
from app.crud.crud_base import CRUDBase
from sqlalchemy.orm import Session
from typing import List

from app.models.partie import Partie
from app.schemas.partie import PartieCreate, PartieUpdate

class CRUDPartie(CRUDBase[Partie, PartieCreate, PartieUpdate]):
    """CRUD spécifique Partie avec méthodes additionnelles si nécessaire"""

    def get_by_dossier(
        self, db: Session, id_dossier: int, skip: int = 0, limit: int = 100
    ) -> List[Partie]:
        """Récupérer les parties par dossier"""
        return db.query(self.model).filter(self.model.id_dossier == id_dossier).offset(skip).limit(limit).all()


# Instance globale
crud_partie = CRUDPartie(Partie)