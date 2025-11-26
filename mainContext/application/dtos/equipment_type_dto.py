from pydantic import BaseModel
from typing import Optional

class EquipmentTypeDTO(BaseModel):
    id: int
    name: Optional[str] = None

class EquipmentTypeCreateDTO(BaseModel):
    name: str

class EquipmentTypeUpdateDTO(BaseModel):
    name: Optional[str] = None
