from pydantic import BaseModel
from typing import Optional

class EquipmentTypeSchema(BaseModel):
    id: int
    name: Optional[str] = None
    
    class Config:
        from_attributes = True

class EquipmentTypeCreateSchema(BaseModel):
    name: str

class EquipmentTypeUpdateSchema(BaseModel):
    name: Optional[str] = None
