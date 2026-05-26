from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json
from app.models.archive import Archive, TypeArchive
from app.schemas.archive import ArchiveCreate, ArchiveUpdate

class CRUDArchive:
    def get(self, db: Session, id: int) -> Optional[Archive]:
        return db.query(Archive).filter(Archive.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Archive]:
        return db.query(Archive).offset(skip).limit(limit).all()

    def get_by_cabinet(self, db: Session, cabinet_id: int, skip: int = 0, limit: int = 100) -> List[Archive]:
        return db.query(Archive).filter(Archive.id_cabinet == cabinet_id).offset(skip).limit(limit).all()

    def get_by_type(self, db: Session, type_archive: TypeArchive, cabinet_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Archive]:
        query = db.query(Archive).filter(Archive.type_archive == type_archive)
        if cabinet_id:
            query = query.filter(Archive.id_cabinet == cabinet_id)
        return query.offset(skip).limit(limit).all()

    def get_by_reference(self, db: Session, type_archive: TypeArchive, id_reference: int) -> Optional[Archive]:
        return db.query(Archive).filter(Archive.type_archive == type_archive, Archive.id_reference == id_reference).first()

    def get_expires_soon(self, db: Session, days: int = 30, cabinet_id: Optional[int] = None) -> List[Archive]:
        date_limite = datetime.utcnow() + timedelta(days=days)
        query = db.query(Archive).filter(Archive.date_suppression_prevue.isnot(None), Archive.date_suppression_prevue <= date_limite)
        if cabinet_id:
            query = query.filter(Archive.id_cabinet == cabinet_id)
        return query.all()

    def create(self, db: Session, obj_in: ArchiveCreate) -> Archive:
        donnees = obj_in.donnees_json
        if isinstance(donnees, dict):
            donnees = json.dumps(donnees)
        db_obj = Archive(
            type_archive=obj_in.type_archive,
            id_reference=obj_in.id_reference,
            id_cabinet=obj_in.id_cabinet,
            dossier_id=obj_in.dossier_id,
            donnees_json=donnees,
            raison_archivage=obj_in.raison_archivage,
            archive_par=obj_in.archive_par,
            date_suppression_prevue=obj_in.date_suppression_prevue
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Archive, obj_in: ArchiveUpdate) -> Archive:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[Archive]:
        obj = db.query(Archive).filter(Archive.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

crud_archive = CRUDArchive()
