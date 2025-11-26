from pydantic import BaseModel
from typing import Optional

class EquipmentBrandSchema(BaseModel):
    id: int
    name: Optional[str] = None
    img_path: Optional[str] = None
    
    class Config:
        from_attributes = True

class EquipmentBrandCreateSchema(BaseModel):
    name: str
    img_path: Optional[str] = None

class EquipmentBrandUpdateSchema(BaseModel):
    name: Optional[str] = None
    img_path: Optional[str] = None
