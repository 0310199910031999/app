from pydantic import BaseModel
from typing import List, Optional



class EquipmentTypeSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class EquipmentBrandSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    img_path: Optional[str] = None

class EquipmentSchema(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    type: Optional[EquipmentTypeSchema] = None
    brand: Optional[EquipmentBrandSchema] = None
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

class UpdateEquipmentSchema(BaseModel):
    type_id: int
    brand_id: int
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



class BrandSchema(BaseModel):
    id : int
    name : str

class TypeSchema(BaseModel):
    id : int
    name : str


class BrandsTypesSchema(BaseModel):
    brands : List[BrandSchema]
    types : List[TypeSchema]
