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

class FOEM01MaterialSchema(BaseModel):
    id : int
    amount : int
    um : str
    part_number : str
    description : Optional[str] = None

class FOEM01Schema(BaseModel):
    id: int
    employee : Optional[EmployeeSchema] = None
    equipment : Optional[EquipmentSchema] = None
    client : Optional[ClientSchema] = None
    file : Optional[FileSchema] = None
    date_created : Optional[date] = None
    hourometer : Optional[float] = None
    status : Optional[str] = None
    reception_name : Optional[str] = None
    signature_path : Optional[str] = None
    date_signed : Optional[date] = None
    materials : Optional[List[FOEM01MaterialSchema]] = None

class FOEM01CreatedSchema(BaseModel):
    equipment_id : int
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"

class FOEM01MaterialUpdateSchema(BaseModel):
    amount : int
    um : str
    part_number : str
    description : Optional[str] = None

class FOEM01UpdateSchema(BaseModel):
    hourometer : float
    reception_name : str
    foem01_materials : List[FOEM01MaterialUpdateSchema]

class FOEM01SignatureSchema(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    signature_base64: str

class FOEM01TableRowSchema(BaseModel):    
    id: int
    file_id : Optional[str] = None
    date_created : date
    employee_name : str
    status : str
    
