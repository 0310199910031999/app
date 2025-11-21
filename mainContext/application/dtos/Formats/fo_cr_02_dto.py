from pydantic import BaseModel
from datetime import date
from typing import Optional


class FOCRAddEquipmentDTO(BaseModel):
    equipment: str
    brand: str
    model: str
    serial_number: str
    equipment_type: str
    economic_number: str
    capability: str
    addition: str


class CreateFOCR02DTO(BaseModel):
    client_id: int
    equipment_id: int
    employee_id: int


class UpdateFOCR02DTO(BaseModel):
    reception_name: Optional[str] = None
    additional_equipment: Optional[FOCRAddEquipmentDTO] = None


class FOCR02SignatureDTO(BaseModel):
    signature_base64: str


class FOCR02TableRowDTO(BaseModel):
    id: int
    status: str
    equipment_name: str
    employee_name: str
    date_created: date
    client_name: Optional[str] = None
    file_id: Optional[str] = None
    file_status: Optional[str] = None
    file_folio: Optional[str] = None
