from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date
from enum import Enum

class TypePaiement(str, Enum):
    FRAIS = "frais"
    AVANCE = "avance"
    RECOUVREMENT = "recouvrement"

class ModePaiement(str, Enum):
    ESPECES = "especes"
    CHEQUE = "cheque"
    VIREMENT = "virement"

class PaiementCreate(BaseModel):
    mot_de_passe: Optional[str] = None
    id_dossier: int
    type_paiement: TypePaiement
    montant: float = Field(..., gt=0)
    date_paiement: date
    mode_paiement: ModePaiement
    reverse_au_client: bool = False

class PaiementUpdate(BaseModel):
    mot_de_passe: Optional[str] = None
    type_paiement: Optional[TypePaiement] = None
    montant: Optional[float] = Field(None, gt=0)
    date_paiement: Optional[date] = None
    mode_paiement: Optional[ModePaiement] = None
    reverse_au_client: Optional[bool] = None

class PaiementResponse(BaseModel):
    mot_de_passe: Optional[str] = None
    id: int
    id_dossier: int
    type_paiement: TypePaiement
    montant: float
    date_paiement: date
    mode_paiement: ModePaiement
    reverse_au_client: bool
    model_config = ConfigDict(from_attributes=True)
