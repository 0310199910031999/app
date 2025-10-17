from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from api.v1.schemas.employee import RoleSchema, EmployeeSchema
from api.v1.schemas.equipment import EquipmentBrandSchema, EquipmentTypeSchema, EquipmentSchema
from api.v1.schemas.Formats.service import ServiceSchema


class FOLE01CreateSchema(BaseModel):
    equipment_id : int
    employee_id : int
    date_created : Optional[date] = date.today()
    status : Optional[str] = "Abierto"

class FOLE01ServiceSchema(BaseModel):
    service_id: int
    diagnose_description: str
    description_service: str
    priority: str

class FOLE01UpdateSchema(BaseModel):
    hourometer: float
    technical_action: str
    reception_name: str
    services: List[FOLE01ServiceSchema]

class FOLE01ServiceSchemaReturn(BaseModel):
    id: int
    service : ServiceSchema
    diagnose_description : str
    description_service : str
    priority: str


class FOLE01Schema(BaseModel):
    id: Optional[int] = None
    employee: Optional[EmployeeSchema] = None
    equipment: Optional[EquipmentSchema] = None
    horometer: Optional[float] = None
    technical_action : Optional[str] = None
    status: Optional[str] = None
    reception_name: Optional[str] = None
    signature_path: Optional[str] = None
    date_signed: Optional[date] = None
    date_created: Optional[date] = None
    rating: Optional[int] = None
    rating_comment: Optional[str] = None
    services : List[FOLE01ServiceSchemaReturn]

class FOLE01TableRawSchema(BaseModel):
    id : int
    economic_number : str
    date_created : date
    codes : List[str]
    employee_name : str
    status : str