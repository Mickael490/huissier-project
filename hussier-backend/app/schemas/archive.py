from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Dict, Any, Union
from datetime import datetime
from app.models.archive import TypeArchive
import json

class ArchiveBase(BaseModel):
    type_archive: TypeArchive
    id_reference: int
    id_cabinet: int
    dossier_id: int
    donnees_json: Union[Dict[str, Any], str]
    raison_archivage: Optional[str] = None
    mot_de_passe: Optional[str] = None
    date_suppression_prevue: Optional[datetime] = None

class ArchiveCreate(ArchiveBase):
    archive_par: int

class ArchiveUpdate(BaseModel):
    raison_archivage: Optional[str] = None
    mot_de_passe: Optional[str] = None
    date_suppression_prevue: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Archive(ArchiveBase):
    id: int
    archive_par: int
    date_archivage: datetime
    model_config = ConfigDict(from_attributes=True)

    @field_validator('donnees_json', mode='before')
    @classmethod
    def parse_donnees_json(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return {}
        return v

class ArchiveDetail(Archive):
    pass
