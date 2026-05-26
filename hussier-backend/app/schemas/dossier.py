from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.dossier import StatutDossier, TypeDossier

class DossierBase(BaseModel):
    objet: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    type_dossier: TypeDossier
    statut: Optional[StatutDossier] = StatutDossier.NOUVEAU
    client_id: Optional[int] = Field(None, gt=0)
    cabinet_id: int = Field(..., gt=0)
    utilisateur_responsable_id: Optional[int] = None
    montant_principal: Optional[Decimal] = Field(None, ge=0)
    montant_frais: Optional[Decimal] = Field(None, ge=0)
    montant_total: Optional[Decimal] = Field(None, ge=0)
    date_ouverture: Optional[datetime] = None
    date_cloture: Optional[datetime] = None
    mot_de_passe: Optional[str] = None
    numero_dossier: Optional[str] = None

    @field_validator('date_ouverture', 'date_cloture', mode='before')
    @classmethod
    def parse_date(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, datetime):
            return v
        try:
            return datetime.fromisoformat(str(v))
        except:
            return None

class DossierCreate(DossierBase):
    pass

class DossierUpdate(BaseModel):
    objet: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    type_dossier: Optional[TypeDossier] = None
    statut: Optional[StatutDossier] = None
    client_id: Optional[int] = Field(None, gt=0)
    utilisateur_responsable_id: Optional[int] = None
    mot_de_passe: Optional[str] = None
    montant_principal: Optional[Decimal] = Field(None, ge=0)
    montant_frais: Optional[Decimal] = Field(None, ge=0)
    montant_total: Optional[Decimal] = Field(None, ge=0)
    date_ouverture: Optional[datetime] = None
    date_cloture: Optional[datetime] = None

    @field_validator('date_ouverture', 'date_cloture', mode='before')
    @classmethod
    def parse_date(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, datetime):
            return v
        try:
            return datetime.fromisoformat(str(v))
        except:
            return None

class DossierResponse(BaseModel):
    id: int
    numero_dossier: Optional[str] = None
    objet: str
    description: Optional[str] = None
    type_dossier: TypeDossier
    statut: StatutDossier
    client_id: Optional[int] = None
    cabinet_id: int
    utilisateur_responsable_id: Optional[int] = None
    montant_principal: Optional[Decimal] = None
    montant_frais: Optional[Decimal] = None
    montant_total: Optional[Decimal] = None
    date_ouverture: Optional[datetime] = None
    date_cloture: Optional[datetime] = None
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    mot_de_passe: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class DossierListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    dossiers: List[DossierResponse]
