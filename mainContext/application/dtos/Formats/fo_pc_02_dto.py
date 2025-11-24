from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# Debido a que no tengo los DTOs para las relaciones, los crearé aquí.
# Estos deberían ser movidos a sus propios archivos eventualmente.


class ClientDTO(BaseModel):
    id: int
    name: str
    rfc : Optional[str] = None
    address : Optional[str] = None
    phone_number : Optional[str] = None
    email : Optional[str] = None
    contact_person : Optional[str] = None

class EquipmentTypeDTO(BaseModel):
    id: int
    name: str

class EquipmentBrandDTO(BaseModel):
    id: int
    name: str

class EquipmentDTO(BaseModel):
    model : str
    serial_number : str
    economic_number : str
    type : EquipmentTypeDTO
    brand : EquipmentBrandDTO  
    mast : str
    hourometer : float
    doh : float
    capacity : str
    addition : str
    motor : str
    property : str

class EmployeeDTO(BaseModel):
    id: int
    name: str
    last_name: str
    email: Optional[str] = None

class CreateFOPC02DTO(BaseModel):
    client_id: int
    employee_id: int
    equipment_id: int
    document_id: int
    document_type: str

class ClientEquipmentPropertyDTO(BaseModel):
    property : Optional[str] = None
    brand : Optional[str] = 'N/A'
    model :  Optional[str] = 'N/A'
    serial_number : Optional[str] = 'N/A'

class UpdateFOPc02DTO(BaseModel):
    departure_date: Optional[datetime] = None
    departure_description: Optional[str] = None

    return_date: Optional[datetime] = None
    return_description: Optional[str] = None

    departure_signature_path: Optional[str] = None
    departure_employee_signature_path: Optional[str] = None

    return_signature_path: Optional[str] = None
    return_employee_signature_path: Optional[str] = None

    name_auth_departure: Optional[str] = None
    name_recipient: Optional[str] = None
    
    observations: Optional[str] = None
    
    property: Optional[ClientEquipmentPropertyDTO] = None


class Fopc02DTO(BaseModel):
    id: int
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
    property: Optional[ClientEquipmentPropertyDTO] = None
    client: Optional[ClientDTO] = None
    employee : Optional[EmployeeDTO] = None
    equipment : Optional[EquipmentDTO] = None

    class Config:
        orm_mode = True

class FOPC02TableRowDTO(BaseModel):
    id: int
    status: str
    file: str
    equipment_name: str
    employee_name: str
    date_created: datetime

class FOPC02SignatureDTO(BaseModel):
    signature_base64: str
    is_departure: bool = False
    is_return: bool = False
    is_employee: bool = False


class GetFOPC02ByDocumentDTO(BaseModel):
    document_id: int
    document_type: str


class FOPC02ByDocumentResponseDTO(BaseModel):
    id: int
    date_created: Optional[datetime] = None
    status: Optional[str] = None
    file_id: Optional[str] = None