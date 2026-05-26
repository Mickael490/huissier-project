# app/crud/crud_statistic.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.statistic import Statistic
from app.schemas.statistic import StatisticCreate, StatisticUpdate


class CRUDStatistic:
    """CRUD pour les statistiques"""

    def get(self, db: Session, id: int) -> Optional[Statistic]:
        """Récupérer une statistique par ID"""
        return db.query(Statistic).filter(Statistic.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Statistic]:
        """Récupérer une liste de statistiques"""
        return (
            db.query(Statistic)
            .order_by(Statistic.calcule_le.desc())  # ✅ CORRIGÉ
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
    ) -> List[Statistic]:
        """Récupérer les statistiques d'un cabinet"""
        return (
            db.query(Statistic)
            .filter(Statistic.id_cabinet == cabinet_id)
            .order_by(Statistic.calcule_le.desc())  # ✅ CORRIGÉ
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_type(
        self,
        db: Session,
        type_statistique: str,
        cabinet_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Statistic]:
        """Récupérer les statistiques par type"""
        query = db.query(Statistic).filter(Statistic.type_statistique == type_statistique)
        
        if cabinet_id:
            query = query.filter(Statistic.id_cabinet == cabinet_id)
        
        return (
            query
            .order_by(Statistic.calcule_le.desc())  # ✅ CORRIGÉ
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, obj_in: StatisticCreate) -> Statistic:
        """Créer une statistique"""
        db_obj = Statistic(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: Statistic,
        obj_in: StatisticUpdate
    ) -> Statistic:
        """Mettre à jour une statistique"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Statistic:
        """Supprimer une statistique"""
        obj = db.query(Statistic).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_dashboard_stats(self, db: Session, cabinet_id: int) -> Dict[str, Any]:
        """Récupérer les statistiques du dashboard"""
        from app.models.dossier import Dossier
        from app.models.client import Client
        from app.models.utilisateur import Utilisateur

        # Statistiques des dossiers
        total_dossiers = db.query(func.count(Dossier.id)).filter(
            Dossier.id_cabinet == cabinet_id
        ).scalar()

        dossiers_actifs = db.query(func.count(Dossier.id)).filter(
            Dossier.id_cabinet == cabinet_id,
            Dossier.statut == "EN_COURS"
        ).scalar()

        # Statistiques des clients
        total_clients = db.query(func.count(Client.id)).filter(
            Client.id_cabinet == cabinet_id
        ).scalar()

        # Statistiques des utilisateurs
        total_utilisateurs = db.query(func.count(Utilisateur.id)).filter(
            Utilisateur.id_cabinet == cabinet_id
        ).scalar()

        return {
            "dossiers": {
                "total": total_dossiers or 0,
                "actifs": dossiers_actifs or 0,
            },
            "clients": {
                "total": total_clients or 0,
            },
            "utilisateurs": {
                "total": total_utilisateurs or 0,
            }
        }

    def get_tendances(
        self,
        db: Session,
        cabinet_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Calculer les tendances sur une période"""
        from app.models.dossier import Dossier

        date_limite = datetime.now() - timedelta(days=days)

        nouveaux = db.query(func.count(Dossier.id)).filter(
            Dossier.id_cabinet == cabinet_id,
            Dossier.date_ouverture >= date_limite
        ).scalar()

        clos = db.query(func.count(Dossier.id)).filter(
            Dossier.id_cabinet == cabinet_id,
            Dossier.statut == "CLOS",
            Dossier.date_cloture >= date_limite
        ).scalar()

        return {
            "periode_jours": days,
            "nouveaux_dossiers": nouveaux or 0,
            "dossiers_clos": clos or 0,
        }


crud_statistic = CRUDStatistic()
