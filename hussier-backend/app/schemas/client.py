from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class TypeClientEnum(str, Enum):
    PARTICULIER = "particulier"
    AVOCAT = "avocat"
    ENTREPRISE = "entreprise"
    JURIDICTION = "juridiction"

class ClientBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=255)
    prenom: Optional[str] = Field(None, max_length=255)
    type_client: TypeClientEnum
    adresse: Optional[str] = None
    telephone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    siret: Optional[str] = Field(None, max_length=14)
    representant_legal: Optional[str] = Field(None, max_length=255)
    mot_de_passe: Optional[str] = None

class ClientCreate(ClientBase):
    cabinet_id: int = Field(..., gt=0)

class ClientUpdate(BaseModel):
    nom: Optional[str] = Field(None, min_length=1, max_length=255)
    prenom: Optional[str] = Field(None, max_length=255)
    type_client: Optional[TypeClientEnum] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    siret: Optional[str] = Field(None, max_length=14)
    representant_legal: Optional[str] = Field(None, max_length=255)
    mot_de_passe: Optional[str] = None

class ClientInDB(ClientBase):
    id: int
    id_cabinet: int
    date_creation: datetime
    date_modification: datetime
    model_config = ConfigDict(from_attributes=True)

class ClientResponse(ClientInDB):
    pass
