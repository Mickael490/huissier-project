from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


class PaiementBase(BaseModel):
    id_dossier: int
    type_paiement: str
    montant: float = Field(..., gt=0)
    date_paiement: date
    mode_paiement: str
    reverse_au_client: bool = False
    mot_de_passe: Optional[str] = None
    numero_cheque: Optional[str] = None
    reference_virement: Optional[str] = None
    reseau_mobile: Optional[str] = None
    numero_mobile: Optional[str] = None
    autre_mode: Optional[str] = None
    note_caisse: Optional[str] = None


class PaiementCreate(PaiementBase):
    pass


class PaiementUpdate(BaseModel):
    id_dossier: Optional[int] = None
    type_paiement: Optional[str] = None
    montant: Optional[float] = Field(None, gt=0)
    date_paiement: Optional[date] = None
    mode_paiement: Optional[str] = None
    reverse_au_client: Optional[bool] = None
    mot_de_passe: Optional[str] = None
    numero_cheque: Optional[str] = None
    reference_virement: Optional[str] = None
    reseau_mobile: Optional[str] = None
    numero_mobile: Optional[str] = None
    autre_mode: Optional[str] = None
    note_caisse: Optional[str] = None


class PaiementResponse(PaiementBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
