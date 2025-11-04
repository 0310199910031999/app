from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from mainContext.application.dtos.client_dto import ClientReadDTO
from mainContext.application.dtos.equipment_dto import EquipmentReadDTO
from api.v1.schemas.employee import EmployeeReadDTO

# Debido a que no tengo los DTOs para las relaciones, los crearé aquí.
# Estos deberían ser movidos a sus propios archivos eventualmente.

class ClientEquipmentPropertyReadDTO(BaseModel):
    id: int
    equipment: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    hourometer: Optional[float] = None
    doh: Optional[float] = None

    class Config:
        orm_mode = True

class FopcServicesReadDTO(BaseModel):
    id: int
    # Agrega aquí los campos de FopcServices que necesites
    class Config:
        orm_mode = True

class Fopp02ReadDTO(BaseModel):
    id: int
    vendor_id: Optional[int] = None
    property_id: Optional[int] = None
    departure_date: Optional[datetime] = None
    departure_description: Optional[str] = None
    delivery_date: Optional[datetime] = None
    delivery_description: Optional[str] = None
    status: Optional[str] = None
    # Agrega otras relaciones si Fopp02 las tiene
    class Config:
        orm_mode = True


class FOPc02BaseDTO(BaseModel):
    departure_date: Optional[datetime] = None
    departure_description: Optional[str] = None
    return_date: Optional[datetime] = None
    return_description: Optional[str] = None
    exit_signature_path: Optional[str] = None
    exit_employee_signature_path: Optional[str] = None
    return_signature_path: Optional[str] = None
    return_employee_signature_path: Optional[str] = None
    status: Optional[str] = None
    name_auth_departure: Optional[str] = None
    name_recipient: Optional[str] = None
    observations: Optional[str] = None


class CreateFOPc02DTO(FOPc02BaseDTO):
    client_id: int
    employee_id: int
    equipment_id: int
    property_id: Optional[int] = None
    fopc_services_id: Optional[int] = None


class UpdateFOPc02DTO(BaseModel):
    departure_date: Optional[datetime] = None
    departure_description: Optional[str] = None
    return_date: Optional[datetime] = None
    return_description: Optional[str] = None
    exit_signature_path: Optional[str] = None
    exit_employee_signature_path: Optional[str] = None
    return_signature_path: Optional[str] = None
    return_employee_signature_path: Optional[str] = None
    status: Optional[str] = None
    name_auth_departure: Optional[str] = None
    name_recipient: Optional[str] = None
    observations: Optional[str] = None
    client_id: Optional[int] = None
    employee_id: Optional[int] = None
    equipment_id: Optional[int] = None
    property_id: Optional[int] = None
    fopc_services_id: Optional[int] = None


class FOPc02ReadDTO(FOPc02BaseDTO):
    id: int
    client: Optional[ClientReadDTO] = None
    employee: Optional[EmployeeReadDTO] = None
    equipment: Optional[EquipmentReadDTO] = None
    property: Optional[ClientEquipmentPropertyReadDTO] = None
    fopc_services: Optional[FopcServicesReadDTO] = None
    fopp02: List[Fopp02ReadDTO] = []

    class Config:
        orm_mode = True