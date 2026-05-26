# app/crud/crud_cabinet.py
from app.models.cabinet import Cabinet
from app.schemas.cabinet import CabinetCreate, CabinetUpdate
from app.crud.crud_base import CRUDBase

class CRUDCabinet(CRUDBase[Cabinet, CabinetCreate, CabinetUpdate]):
    """
    CRUD spécifique pour Cabinet
    On peut ajouter ici des méthodes propres aux Cabinets
    """
    pass

crud_cabinet = CRUDCabinet(Cabinet)