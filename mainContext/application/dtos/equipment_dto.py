from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel

@dataclass
class EquipmentDTO:
    id: int
    client_id: int
    type_id: int
    type_name: str
    brand_id: int
    brand_name: str
    brand_img_path: str
    model: str
    mast: str
    serial_number: str
    hourometer: float
    doh: float
    economic_number: str
    capacity: str
    addition: str
    motor: str
    property: str


class EquipmentInfoDTO(BaseModel):
    """Lightweight Equipment info for nested responses"""
    id: int
    model: Optional[str] = None
    serial_number: Optional[str] = None
    economic_number: Optional[str] = None
    brand_name: Optional[str] = None
