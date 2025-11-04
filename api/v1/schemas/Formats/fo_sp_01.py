from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from api.v1.schemas.equipment import EquipmentBrandSchema, EquipmentTypeSchema, EquipmentSchema
from api.v1.schemas.client import ClientInfoSchema as ClientSchema
from api.v1.schemas.Formats.service import ServiceSchema




class FOSP01ServiceSchema(BaseModel):
    id : int
    service : ServiceSchema

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

class FOSP01Schema(BaseModel):
    id : int
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
    fopc_services_id : Optional[int] = None
    services : Optional[List[FOSP01ServiceSchema]] = None
    GC : Optional[str] = None


class FOSP01CreateSchema(BaseModel):
    employee_id : int
    equipment_id : int 
    date_created : date = date.today()
    status : str = "Abierto"
    GC : Optional[str] = None



#Update Schemas
class FOSP01ServiceSchema(BaseModel):
    service_id: int

class FOSP01UpdateSchema(BaseModel): 
    hourometer : float 
    observations : str
    reception_name : str
    fosp01_services : Optional[List[FOSP01ServiceSchema]] = None
    evidence_photos_before_base64 : Optional[List[str]] = None
    evidence_photos_after_base64 : Optional[List[str]] = None



#Signed Schema
class FOSP01SignatureSchema(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : str
    signature_base64: str
    


#Table Row Schema
class FOSP01TableRowSchema(BaseModel):
    id: int
    date_created : date
    file_id : Optional[str] = None
    observations: Optional[str] = None
    codes : Optional[List[str]]= None
    employee_name : str
    status : str