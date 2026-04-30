from pydantic import BaseModel
from datetime import date
from typing import List, Optional
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


class FOEM011MaterialSchema(BaseModel):
    id : int
    amount : int
    um : str
    part_number : str
    description : Optional[str] = None


class FOEM011Schema(BaseModel):
    id: int
    employee : Optional[EmployeeSchema] = None
    client : Optional[ClientSchema] = None
    file : Optional[FileSchema] = None
    date_created : Optional[date] = None
    hourometer : Optional[float] = None
    status : Optional[str] = None
    reception_name : Optional[str] = None
    signature_path : Optional[str] = None
    date_signed : Optional[date] = None
    materials : Optional[List[FOEM011MaterialSchema]] = None
    observations : Optional[str] = None
    rating : Optional[int] = None
    rating_comment : Optional[str] = None
    evidence_photos : Optional[List[str]] = None


class FOEM011CreatedSchema(BaseModel):
    client_id : int
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"


class FOEM011MaterialUpdateSchema(BaseModel):
    amount : int
    um : str
    part_number : str
    description : Optional[str] = None


class FOEM011UpdateSchema(BaseModel):
    hourometer : float
    reception_name : str
    employee_id : int
    observations : Optional[str] = None
    foem01_1_materials : List[FOEM011MaterialUpdateSchema]
    evidence_photos_base64 : Optional[List[str]] = None


class FOEM011SignatureSchema(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    signature_base64: str
    employee_id: int
    rating : int
    rating_comment : Optional[str] = None


class FOEM011TableRowSchema(BaseModel):
    id: int
    file_id : Optional[str] = None
    date_created : date
    employee_name : str
    status : str
    rating : Optional[int] = None
    rating_comment : Optional[str] = None