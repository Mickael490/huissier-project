from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.audit_log import ActionType, EntityType


class AuditLogBase(BaseModel):
    action: ActionType
    entity_type: EntityType
    entity_id: Optional[int] = None
    id_cabinet: Optional[int] = None
    id_utilisateur: Optional[int] = None
    description: Optional[str] = None
    donnees_avant: Optional[Dict[str, Any]] = None
    donnees_apres: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLog(AuditLogBase):
    id: int
    date_action: datetime
    model_config = ConfigDict(from_attributes=True)


class AuditLogDetail(AuditLog):
    pass
