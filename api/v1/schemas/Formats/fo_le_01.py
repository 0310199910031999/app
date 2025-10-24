from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from api.v1.schemas.employee import RoleSchema
from api.v1.schemas.equipment import EquipmentBrandSchema, EquipmentTypeSchema, EquipmentSchema
from api.v1.schemas.client import ClientInfoSchema as ClientSchema
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
    fole01_services: Optional[List[FOLE01ServiceSchema]] = None
    evidence_photos_base64: Optional[List[str]] = None


class FOLE01ServiceSchema(BaseModel):
    id: int
    service : ServiceSchema
    diagnose_description : str
    description_service : str
    priority: str

class EmployeeSchema(BaseModel):
    id : Optional[int] = None
    role : Optional[RoleSchema] = None
    name : Optional[str] = None
    lastname: Optional[str] = None

class FOLE01Schema(BaseModel):
    id: Optional[int] = None
    employee: Optional[EmployeeSchema] = None
    equipment: Optional[EquipmentSchema] = None
    client: Optional[ClientSchema] = None
    horometer: Optional[float] = None
    technical_action : Optional[str] = None
    status: Optional[str] = None
    reception_name: Optional[str] = None
    signature_path: Optional[str] = None
    date_signed: Optional[date] = None
    date_created: Optional[date] = None
    rating: Optional[int] = None
    rating_comment: Optional[str] = None
    services : Optional[List[FOLE01ServiceSchema]]

class FOLE01TableRowSchema(BaseModel):
    id : int
    date_created : date
    codes : Optional[List[str]] = None
    employee_name : str
    status : str

class FOLE01SignatureSchema(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : Optional[str] = None
    signature_base64: str