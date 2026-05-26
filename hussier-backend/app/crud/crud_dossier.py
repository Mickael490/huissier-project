# app/crud/crud_dossier.py
from typing import Optional, List
from sqlalchemy import func
from app.crud.crud_base import CRUDBase
from sqlalchemy.orm import Session
from app.models.dossier import Dossier, StatutDossier, TypeDossier
from app.schemas.dossier import DossierCreate, DossierUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CRUDDossier(CRUDBase[Dossier, DossierCreate, DossierUpdate]):

    def get_by_numero(self, db: Session, numero_dossier: str) -> Optional[Dossier]:
        return db.query(self.model).filter(Dossier.numero_dossier == numero_dossier).first()

    def update(self, db: Session, db_obj: Dossier, obj_in) -> Dossier:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "mot_de_passe" in update_data and update_data["mot_de_passe"]:
            update_data["mot_de_passe"] = pwd_context.hash(update_data["mot_de_passe"])
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def verrouiller_dossier(self, db: Session, dossier_id: int, mot_de_passe: str):
        dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()
        if not dossier:
            return None
        dossier.mot_de_passe = pwd_context.hash(mot_de_passe)
        db.commit()
        db.refresh(dossier)
        return dossier

    def deverrouiller_dossier(self, db: Session, dossier_id: int, mot_de_passe: str):
        dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()
        if not dossier:
            return None, "dossier_introuvable"
        if not dossier.mot_de_passe:
            return None, "non_verrouille"
        if not pwd_context.verify(mot_de_passe, dossier.mot_de_passe):
            return None, "mot_de_passe_incorrect"
        dossier.mot_de_passe = None
        db.commit()
        db.refresh(dossier)
        return dossier, "ok"

    def cloturer_dossier(self, db: Session, dossier_id: int) -> Optional[Dossier]:
        dossier = self.get(db, dossier_id)
        if not dossier:
            return None
        dossier.statut = StatutDossier.TERMINE
        db.commit()
        db.refresh(dossier)
        return dossier

    def archiver_dossier(self, db: Session, dossier_id: int) -> Optional[Dossier]:
        dossier = self.get(db, dossier_id)
        if not dossier:
            return None
        dossier.statut = StatutDossier.ARCHIVE
        db.commit()
        db.refresh(dossier)
        return dossier

    def compter_dossiers_par_statut(self, db: Session, cabinet_id: Optional[int] = None) -> dict:
        query = db.query(Dossier.statut, func.count(Dossier.id)).group_by(Dossier.statut)
        if cabinet_id:
            query = query.filter(Dossier.cabinet_id == cabinet_id)
        return dict(query.all())

    def compter_dossiers_par_type(self, db: Session, cabinet_id: Optional[int] = None) -> dict:
        query = db.query(Dossier.type_dossier, func.count(Dossier.id)).group_by(Dossier.type_dossier)
        if cabinet_id:
            query = query.filter(Dossier.cabinet_id == cabinet_id)
        return dict(query.all())


crud_dossier = CRUDDossier(Dossier)