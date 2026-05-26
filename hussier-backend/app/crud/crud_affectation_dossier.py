# app/crud/crud_affectation_dossier.py
from typing import List, Optional
from app.crud.crud_base import CRUDBase
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.affectation_dossier import AffectationDossier
from app.schemas.affectation_dossier import AffectationDossierCreate, AffectationDossierUpdate


class CRUDAffectationDossier(CRUDBase[AffectationDossier, AffectationDossierCreate, AffectationDossierUpdate]):

    def get_by_dossier(self, db: Session, dossier_id: int, actives_only: bool = False) -> List[AffectationDossier]:
        """Récupérer les affectations d'un dossier"""
        query = db.query(self.model).filter(self.model.id_dossier == dossier_id)
        if actives_only:
            query = query.filter(self.model.date_fin.is_(None))
        return query.order_by(self.model.date_affectation.desc()).all()

    def get_active_by_dossier(self, db: Session, dossier_id: int) -> Optional[AffectationDossier]:
        """Récupérer l'affectation active d'un dossier"""
        return (
            db.query(self.model)
            .filter(self.model.id_dossier == dossier_id, self.model.date_fin.is_(None))
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        utilisateur_id: int,
        actives_only: bool = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[AffectationDossier]:
        """Récupérer les affectations d'un utilisateur"""
        query = db.query(self.model).filter(self.model.id_utilisateur == utilisateur_id)
        if actives_only:
            query = query.filter(self.model.date_fin.is_(None))
        return query.order_by(self.model.date_affectation.desc()).offset(skip).limit(limit).all()

    def deactivate(self, db: Session, affectation_id: int, raison: str) -> Optional[AffectationDossier]:
        """Désactiver (terminer) une affectation"""
        obj = self.get(db, affectation_id)
        if obj and not obj.date_fin:
            obj.date_fin = datetime.utcnow()
            obj.raison_desaffectation = raison
            db.commit()
            db.refresh(obj)
        return obj

    def reactivate(self, db: Session, affectation_id: int) -> Optional[AffectationDossier]:
        """Réactiver une affectation (supprime date_fin)"""
        obj = self.get(db, affectation_id)
        if obj and obj.date_fin:
            obj.date_fin = None
            obj.raison_desaffectation = None
            db.commit()
            db.refresh(obj)
        return obj

    def reassign_dossier(
        self,
        db: Session,
        dossier_id: int,
        old_user_id: int,
        new_user_id: int,
        affecte_par: int,
        raison_desaffectation: Optional[str] = None
    ) -> Optional[AffectationDossier]:
        """Réaffecter un dossier à un nouvel utilisateur"""
        # Désactiver l'affectation existante
        old_aff = self.get_by_dossier_and_user(db, dossier_id, old_user_id)
        if old_aff and old_aff.date_fin is None:
            self.deactivate(db, old_aff.id, raison=raison_desaffectation or "Réaffectation")

        # Créer la nouvelle affectation
        obj_in = AffectationDossierCreate(
            id_dossier=dossier_id,
            id_utilisateur=new_user_id,
            affecte_par=affecte_par,
            commentaire="Réaffectation"
        )
        return self.create(db, obj_in)

    def get_by_dossier_and_user(self, db: Session, dossier_id: int, user_id: int) -> Optional[AffectationDossier]:
        """Récupérer une affectation par dossier et utilisateur"""
        return (
            db.query(self.model)
            .filter(self.model.id_dossier == dossier_id, self.model.id_utilisateur == user_id)
            .order_by(self.model.date_affectation.desc())
            .first()
        )


crud_affectation_dossier = CRUDAffectationDossier(AffectationDossier)