from pydantic import BaseModel
from datetime import date
from typing import List, Optional

from api.v1.schemas.equipment import EquipmentBrandSchema, EquipmentTypeSchema, EquipmentSchema
from api.v1.schemas.client import ClientInfoSchema as ClientSchema


class RoleSchema(BaseModel):
    id: int
    role_name: str

class EmployeeSchema(BaseModel):
    id : Optional[int] = None
    role : Optional[RoleSchema] = None
    name : Optional[str] = None
    lastname: Optional[str] = None

class FileSchema(BaseModel):
    id: str
    folio: Optional[str]

class FOBC01Schema(BaseModel):
    id: int
    employee : Optional[EmployeeSchema] = None
    equipment : Optional[EquipmentSchema] = None
    client : Optional[ClientSchema] = None
    file : Optional[FileSchema] = None
    date_created : Optional[date] = None
    hourometer : Optional[float] = None
    observations : Optional[str] = None
    status : Optional[str] = None
    reception_name : Optional[str] = None
    signature_path : Optional[str] = None
    date_signed : Optional[date] = None
    rating : Optional[int] = None
    rating_comment : Optional[str] = None

class FOBC01CreateSchema(BaseModel):
    equipment_id : int
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"

class FOBC01UpdateSchema(BaseModel):
    hourometer : float
    observations : str
    reception_name : str

class FOBC01SignatureSchema(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : str
    signature_base64: str

class FOBC01TableRowSchema(BaseModel):
    id: int
    file_id : Optional[str] = None
    date_created : date
    observations: Optional[str] = None
    employee_name : Optional[str] = "N/A"
    status : str