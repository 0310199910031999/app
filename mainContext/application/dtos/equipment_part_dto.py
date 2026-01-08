from typing import Optional
from pydantic import BaseModel


class EquipmentPartDTO(BaseModel):
    id: int
    part_number: str
    description: str
    amount: Optional[int] = None
    equipment_id: int

    class Config:
        from_attributes = True


class EquipmentPartCreateDTO(BaseModel):
    part_number: str
    description: str
    amount: Optional[int] = None
    equipment_id: int


class EquipmentPartUpdateDTO(BaseModel):
    part_number: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[int] = None
    equipment_id: Optional[int] = None
