# app/crud/crud_agenda.py
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.agenda import Agenda
from app.schemas.agenda import AgendaCreate, AgendaUpdate


class CRUDAgenda:
    """CRUD pour l'agenda"""

    def generate_reference(self, db: Session) -> str:
        """Générer une référence unique pour le rendez-vous"""
        prefix = f"RDV-{datetime.now().strftime('%Y%m')}"
        
        last_rdv = (
            db.query(Agenda)
            .filter(Agenda.reference.like(f"{prefix}%"))
            .order_by(Agenda.id.desc())
            .first()
        )
        
        if last_rdv and last_rdv.reference:
            try:
                last_num = int(last_rdv.reference.split("-")[-1])
                new_num = last_num + 1
            except (ValueError, IndexError):
                new_num = 1
        else:
            new_num = 1
        
        return f"{prefix}-{new_num:04d}"

    def create(self, db: Session, *, obj_in: AgendaCreate) -> Agenda:
        """Créer un nouveau rendez-vous avec référence auto-générée"""
        reference = self.generate_reference(db)
        
        db_obj = Agenda(
            reference=reference,
            **obj_in.model_dump()
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[Agenda]:
        """Récupérer un rendez-vous par son ID"""
        return db.query(Agenda).filter(Agenda.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Agenda]:
        """Récupérer plusieurs rendez-vous"""
        return (
            db.query(Agenda)
            .order_by(Agenda.date_debut.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: Agenda,
        obj_in: AgendaUpdate
    ) -> Agenda:
        """Mettre à jour un rendez-vous"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> bool:
        """Supprimer un rendez-vous"""
        obj = db.query(Agenda).filter(Agenda.id == id).first()
        
        if not obj:
            return False
        
        db.delete(obj)
        db.commit()
        return True

    def get_by_reference(self, db: Session, *, reference: str) -> Optional[Agenda]:
        """Récupérer un rendez-vous par sa référence"""
        return db.query(Agenda).filter(Agenda.reference == reference).first()

    def get_by_utilisateur(
        self,
        db: Session,
        *,
        utilisateur_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Agenda]:
        """Récupérer les rendez-vous d'un utilisateur"""
        return (
            db.query(Agenda)
            .filter(Agenda.id_utilisateur == utilisateur_id)
            .order_by(Agenda.date_debut.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_dossier(
        self,
        db: Session,
        *,
        dossier_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Agenda]:
        """Récupérer les rendez-vous d'un dossier"""
        return (
            db.query(Agenda)
            .filter(Agenda.id_dossier == dossier_id)
            .order_by(Agenda.date_debut.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_client(
        self,
        db: Session,
        *,
        client_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Agenda]:
        """Récupérer les rendez-vous d'un client"""
        return (
            db.query(Agenda)
            .filter(Agenda.id_client == client_id)
            .order_by(Agenda.date_debut.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_period(
        self,
        db: Session,
        *,
        date_debut: datetime,
        date_fin: datetime,
        utilisateur_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Agenda]:
        """Récupérer les rendez-vous d'une période"""
        query = db.query(Agenda).filter(
            Agenda.date_debut >= date_debut,
            Agenda.date_fin <= date_fin
        )
        
        if utilisateur_id:
            query = query.filter(Agenda.id_utilisateur == utilisateur_id)
        
        return (
            query
            .order_by(Agenda.date_debut)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def annuler(
        self,
        db: Session,
        *,
        db_obj: Agenda,
        motif: str
    ) -> Agenda:
        """Annuler un rendez-vous"""
        db_obj.annule = True
        db_obj.motif_annulation = motif
        db_obj.date_annulation = datetime.utcnow()
        db_obj.statut = "annule"
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def reporter(
        self,
        db: Session,
        *,
        db_obj: Agenda,
        nouvelle_date_debut: datetime,
        nouvelle_date_fin: datetime
    ) -> Agenda:
        """Reporter un rendez-vous"""
        db_obj.ancienne_date = db_obj.date_debut
        db_obj.reporte = True
        db_obj.date_debut = nouvelle_date_debut
        db_obj.date_fin = nouvelle_date_fin
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_agenda = CRUDAgenda()
