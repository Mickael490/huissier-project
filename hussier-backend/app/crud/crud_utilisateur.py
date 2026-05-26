from typing import Optional
from app.crud.crud_base import CRUDBase
from sqlalchemy.orm import Session
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate
from app.core.security import get_password_hash

class CRUDUtilisateur(CRUDBase[Utilisateur, UtilisateurCreate, UtilisateurUpdate]):

    def get_by_email(self, db: Session, email: str) -> Optional[Utilisateur]:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, obj_in: UtilisateurCreate) -> Utilisateur:
        obj_data = obj_in.model_dump()
        mot_de_passe = obj_data.pop("mot_de_passe")
        obj_data["mot_de_passe_hash"] = get_password_hash(mot_de_passe)
        obj_data["id_cabinet"] = obj_data.pop("id_cabinet", 1)
        db_obj = Utilisateur(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Utilisateur, obj_in: UtilisateurUpdate) -> Utilisateur:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "mot_de_passe" in update_data:
            update_data["mot_de_passe_hash"] = get_password_hash(update_data.pop("mot_de_passe"))
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_utilisateur = CRUDUtilisateur(Utilisateur)
