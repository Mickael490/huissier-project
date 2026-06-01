from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from enum import Enum

class TypePaiement(str, Enum):
    FRAIS = "frais"
    AVANCE = "avance"
    
    PROVISION = "provision"
    SOLDE = "solde"
    RECOUVREMENT = "recouvrement"

class ModePaiement(str, Enum):
    ESPECES = "especes"
    CHEQUE = "cheque"
    VIREMENT = "virement"
    MOBILE = "mobile"
    AUTRE = "autre"

class PaiementCreate(BaseModel):
    id_dossier: int
    type_paiement: str
    montant: float = Field(..., gt=0)
    date_paiement: date
    mode_paiement: str
    reverse_au_client: bool = False
    mot_de_passe: Optional[str] = None
    # Champs conditionnels
    numero_cheque: Optional[str] = None
    reference_virement: Optional[str] = None
    reseau_mobile: Optional[str] = None  # MTN, Orange, Coris, Moov, Wave
    numero_mobile: Optional[str] = None
    autre_mode: Optional[str] = None

class PaiementUpdate(BaseModel):
    type_paiement: Optional[TypePaiement] = None
    montant: Optional[float] = Field(None, gt=0)
    date_paiement: Optional[date] = None
    mode_paiement: Optional[ModePaiement] = None
    reverse_au_client: Optional[bool] = None
    mot_de_passe: Optional[str] = None
    numero_cheque: Optional[str] = None
    reference_virement: Optional[str] = None
    reseau_mobile: Optional[str] = None
    numero_mobile: Optional[str] = None
    autre_mode: Optional[str] = None

class PaiementResponse(BaseModel):
    id: int
    id_dossier: int
    type_paiement: str
    montant: float
    date_paiement: date
    mode_paiement: str
    reverse_au_client: bool
    mot_de_passe: Optional[str] = None
    numero_cheque: Optional[str] = None
    reference_virement: Optional[str] = None
    reseau_mobile: Optional[str] = None
    numero_mobile: Optional[str] = None
    autre_mode: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
