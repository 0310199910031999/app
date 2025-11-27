from pydantic import BaseModel
from typing import Optional

class EquipmentTypeDTO(BaseModel):
    id: int
    name: Optional[str] = None

class EquipmentBrandDTO(BaseModel):
    id: int
    name: Optional[str] = None
    img_path: Optional[str] = None

class EquipmentByPropertyDTO(BaseModel):
    id: int
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    type: Optional[EquipmentTypeDTO] = None
    brand: Optional[EquipmentBrandDTO] = None
    model: Optional[str] = None
    mast: Optional[str] = None
    serial_number: Optional[str] = None
    hourometer: Optional[float] = None
    doh: Optional[float] = None
    economic_number: Optional[str] = None
    capacity: Optional[str] = None
    addition: Optional[str] = None
    motor: Optional[str] = None
    property: Optional[str] = None
