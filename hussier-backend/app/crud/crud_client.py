# app/crud/crud_client.py
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class CRUDClient:
    """CRUD pour les clients"""
    
    def create(self, db: Session, obj_in: ClientCreate) -> Client:
        """Créer un nouveau client"""
        db_client = Client(
            id_cabinet=obj_in.cabinet_id,  # ← Conversion cabinet_id → id_cabinet
            nom=obj_in.nom,
            prenom=obj_in.prenom,
            type_client=obj_in.type_client,
            adresse=obj_in.adresse,
            telephone=obj_in.telephone,
            email=obj_in.email,
            siret=obj_in.siret,
            representant_legal=obj_in.representant_legal
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    def get(self, db: Session, id: int) -> Optional[Client]:
        """Récupérer un client par son ID"""
        return db.query(Client).filter(Client.id == id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[Client]:
        """Récupérer un client par email"""
        return db.query(Client).filter(Client.email == email).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        cabinet_id: Optional[int] = None,
        type_client: Optional[str] = None
    ) -> List[Client]:
        """Récupérer une liste de clients avec filtres optionnels"""
        query = db.query(Client)
        
        if cabinet_id:
            query = query.filter(Client.id_cabinet == cabinet_id)
        
        if type_client:
            query = query.filter(Client.type_client == type_client)
        
        return query.offset(skip).limit(limit).all()

    def update(
        self,
        db: Session,
        db_obj: Client,
        obj_in: ClientUpdate
    ) -> Client:
        """Mettre à jour un client"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[Client]:
        """Supprimer un client"""
        db_client = self.get(db, id)
        
        if db_client:
            db.delete(db_client)
            db.commit()
        
        return db_client


crud_client = CRUDClient()
