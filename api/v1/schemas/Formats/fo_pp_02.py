from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class VendorSchema(BaseModel):
    id: int
    name: str
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    rfc: Optional[str] = None


class EmployeeSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None


class ClientEquipmentPropertySchema(BaseModel):
    id: Optional[int] = None
    property: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None


class FOPP02Schema(BaseModel):
    id: int
    vendor_id: Optional[int] = None
    property_id: Optional[int] = None
    departure_date: Optional[datetime] = None
    departure_description: Optional[str] = None
    delivery_date: Optional[datetime] = None
    delivery_description: Optional[str] = None
    departure_signature_path: Optional[str] = None
    departure_employee_signature_path: Optional[str] = None
    delivery_signature_path: Optional[str] = None
    delivery_employee_signature_path: Optional[str] = None
    observations: Optional[str] = None
    employee_id: Optional[int] = None
    status: Optional[str] = None
    name_auth_departure: Optional[str] = None
    name_delivery: Optional[str] = None
    fopc_id: Optional[int] = None
    file_id: Optional[str] = None
    date_created: Optional[datetime] = None
    employee: Optional[EmployeeSchema] = None
    property: Optional[ClientEquipmentPropertySchema] = None
    vendor: Optional[VendorSchema] = None


class FOPP02CreateSchema(BaseModel):
    employee_id: int
    fopc_id: int
    property_id: int
    status: str = "Abierto"
    file_id: Optional[str] = None


class FOPP02UpdateSchema(BaseModel):
    departure_date: Optional[datetime] = None
    departure_description: Optional[str] = None
    delivery_date: Optional[datetime] = None
    delivery_description: Optional[str] = None
    name_auth_departure: Optional[str] = None
    name_delivery: Optional[str] = None
    observations: Optional[str] = None
    vendor_id: Optional[int] = None


class FOPP02SignatureSchema(BaseModel):
    signature_base64: str
    is_employee: bool = False  # True si es firma de empleado, False si es de cliente


class FOPP02TableRowSchema(BaseModel):
    id: int
    status: str
    file: str
    equipment_name: str
    employee_name: str
    date_created: datetime


class GetFOPP02ByFOPCSchema(BaseModel):
    fopc_id: int


class FOPP02ByFOPCResponseSchema(BaseModel):
    id: int
    date_created: Optional[datetime] = None
    status: Optional[str] = None
    file_id: Optional[str] = None
