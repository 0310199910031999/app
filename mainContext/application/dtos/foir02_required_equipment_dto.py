from pydantic import BaseModel
from typing import Optional

class Foir02RequiredEquipmentDTO(BaseModel):
    id: int
    amount: Optional[int] = None
    unit: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None

class Foir02RequiredEquipmentCreateDTO(BaseModel):
    amount: int
    unit: str
    type: str
    name: str

class Foir02RequiredEquipmentUpdateDTO(BaseModel):
    amount: Optional[int] = None
    unit: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
