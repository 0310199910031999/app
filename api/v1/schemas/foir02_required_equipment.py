from pydantic import BaseModel
from typing import Optional

class Foir02RequiredEquipmentSchema(BaseModel):
    id: int
    amount: Optional[int] = None
    unit: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    
    class Config:
        from_attributes = True

class Foir02RequiredEquipmentCreateSchema(BaseModel):
    amount: int
    unit: str
    type: str
    name: str

class Foir02RequiredEquipmentUpdateSchema(BaseModel):
    amount: Optional[int] = None
    unit: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
