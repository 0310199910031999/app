from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from api.v1.schemas.equipment import EquipmentSchema
from api.v1.schemas.client import ClientInfoSchema as ClientSchema

class RoleSchema(BaseModel):
    id: int
    role_name: str

class EmployeeSchema(BaseModel):
    id: Optional[int] = None
    role: Optional[RoleSchema] = None
    name: Optional[str] = None
    lastname: Optional[str] = None

class ClientEquipmentPropertySchema(BaseModel):
    id: Optional[int] = None
    property: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None

class FOPC02Schema(BaseModel):
    id: int
    client: Optional[ClientSchema] = None
    employee: Optional[EmployeeSchema] = None
    equipment: Optional[EquipmentSchema] = None
    property: Optional[ClientEquipmentPropertySchema] = None
    departure_date: Optional[datetime] = None
    departure_description: Optional[str] = None
    return_date: Optional[datetime] = None
    return_description: Optional[str] = None
    departure_signature_path: Optional[str] = None
    departure_employee_signature_path: Optional[str] = None
    return_signature_path: Optional[str] = None
    return_employee_signature_path: Optional[str] = None
    status: Optional[str] = None
    name_auth_departure: Optional[str] = None
    name_recipient: Optional[str] = None
    observations: Optional[str] = None
    file_id: Optional[str] = None
    fopc_services_id: Optional[int] = None

class FOPC02CreateSchema(BaseModel):
    client_id: int
    employee_id: int
    equipment_id: int
    document_id: int
    document_type: str  # 'foos01', 'fosp01', o 'fosc01'

class ClientEquipmentPropertyUpdateSchema(BaseModel):
    property: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None

class FOPC02UpdateSchema(BaseModel):
    departure_date: Optional[datetime] = None
    departure_description: Optional[str] = None
    return_date: Optional[datetime] = None
    return_description: Optional[str] = None
    name_auth_departure: Optional[str] = None
    name_recipient: Optional[str] = None
    observations: Optional[str] = None
    property: Optional[ClientEquipmentPropertyUpdateSchema] = None

class FOPC02SignatureSchema(BaseModel):
    signature_base64: str
    is_employee: bool = False  # True si es firma de empleado, False si es de cliente

class FOPC02TableRowSchema(BaseModel):
    id: int
    status: str
    file: str
    equipment_name: str
    employee_name: str
    date_created: datetime


class GetFOPC02ByDocumentSchema(BaseModel):
    document_id: int
    document_type: str  # 'foos01', 'fosp01', o 'fosc01'


class FOPC02ByDocumentResponseSchema(BaseModel):
    id: int
    date_created: Optional[datetime] = None
    status: Optional[str] = None
    file_id: Optional[str] = None
