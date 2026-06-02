# app/crud/crud_audit_log.py
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.audit_log import AuditLog, ActionType
from app.schemas.audit_log import AuditLogCreate


class CRUDAuditLog:
    """CRUD pour les logs d'audit"""

    def get(self, db: Session, id: int) -> Optional[AuditLog]:
        """Récupérer un log par ID"""
        return db.query(AuditLog).filter(AuditLog.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Récupérer une liste de logs"""
        return (
            db.query(AuditLog)
            .order_by(AuditLog.date_action.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_cabinet(
        self,
        db: Session,
        cabinet_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Récupérer les logs d'un cabinet"""
        return (
            db.query(AuditLog)
            .filter(AuditLog.id_cabinet == cabinet_id)
            .order_by(AuditLog.date_action.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Récupérer les logs d'un utilisateur"""
        return (
            db.query(AuditLog)
            .filter(AuditLog.id_utilisateur == user_id)
            .order_by(AuditLog.date_action.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_action_type(
        self,
        db: Session,
        action_type: ActionType,
        cabinet_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Récupérer les logs par type d'action"""
        query = db.query(AuditLog).filter(AuditLog.action == action_type)

        if cabinet_id:
            query = query.filter(AuditLog.id_cabinet == cabinet_id)

        return (
            query.order_by(AuditLog.date_action.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_entity(
        self,
        db: Session,
        entity_type: str,
        entity_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Récupérer les logs d'un type d'entité (et éventuellement d'un enregistrement)"""
        query = db.query(AuditLog).filter(AuditLog.entity_type == entity_type)

        if entity_id:
            query = query.filter(AuditLog.entity_id == entity_id)

        return (
            query.order_by(AuditLog.date_action.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_date_range(
        self,
        db: Session,
        date_debut: datetime,
        date_fin: datetime,
        cabinet_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Récupérer les logs sur une période"""
        query = db.query(AuditLog).filter(
            AuditLog.date_action >= date_debut,
            AuditLog.date_action <= date_fin
        )
        
        if cabinet_id:
            query = query.filter(AuditLog.id_cabinet == cabinet_id)
        
        return (
            query.order_by(AuditLog.date_action.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_recent(
        self,
        db: Session,
        hours: int = 24,
        cabinet_id: Optional[int] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """Récupérer les logs récents"""
        date_limite = datetime.utcnow() - timedelta(hours=hours)
        query = db.query(AuditLog).filter(AuditLog.date_action >= date_limite)
        
        if cabinet_id:
            query = query.filter(AuditLog.id_cabinet == cabinet_id)
        
        return (
            query.order_by(AuditLog.date_action.desc())
            .limit(limit)
            .all()
        )

    def create(self, db: Session, obj_in: AuditLogCreate) -> AuditLog:
        """Créer un nouveau log d'audit"""
        db_obj = AuditLog(
            action=obj_in.action,
            entity_type=obj_in.entity_type,
            entity_id=obj_in.entity_id,
            id_cabinet=obj_in.id_cabinet,
            id_utilisateur=obj_in.id_utilisateur,
            description=obj_in.description,
            donnees_avant=obj_in.donnees_avant,
            donnees_apres=obj_in.donnees_apres,
            ip_address=obj_in.ip_address,
            user_agent=obj_in.user_agent
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_old_logs(
        self,
        db: Session,
        days: int = 365,
        cabinet_id: Optional[int] = None
    ) -> int:
        """Supprimer les logs anciens"""
        date_limite = datetime.utcnow() - timedelta(days=days)
        query = db.query(AuditLog).filter(AuditLog.date_action < date_limite)
        
        if cabinet_id:
            query = query.filter(AuditLog.id_cabinet == cabinet_id)
        
        count = query.count()
        query.delete(synchronize_session=False)
        db.commit()
        return count


crud_audit_log = CRUDAuditLog()
