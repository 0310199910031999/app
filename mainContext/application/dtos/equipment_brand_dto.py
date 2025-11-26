from pydantic import BaseModel
from typing import Optional

class EquipmentBrandDTO(BaseModel):
    id: int
    name: Optional[str] = None
    img_path: Optional[str] = None

class EquipmentBrandCreateDTO(BaseModel):
    name: str
    img_path: Optional[str] = None

class EquipmentBrandUpdateDTO(BaseModel):
    name: Optional[str] = None
    img_path: Optional[str] = None
