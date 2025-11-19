from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class EmployeeSimpleSchema(BaseModel):
    id: int
    name: Optional[str] = None
    lastname: Optional[str] = None
    
    class Config:
        from_attributes = True


class EquipmentSimpleSchema(BaseModel):
    id: int
    model: Optional[str] = None
    
    class Config:
        from_attributes = True


class ClientSimpleSchema(BaseModel):
    id: int
    name: Optional[str] = None
    
    class Config:
        from_attributes = True


class FOCRAddEquipmentSchema(BaseModel):
    equipment: str
    brand: str
    model: str
    serial_number: str
    equipment_type: str
    economic_number: str
    capability: str
    addition: str
    
    class Config:
        from_attributes = True


class CreateFOCR02Schema(BaseModel):
    client_id: int
    equipment_id: int
    employee_id: int
    
    class Config:
        from_attributes = True


class UpdateFOCR02Schema(BaseModel):
    equipment_id: Optional[int] = None
    employee_id: Optional[int] = None
    reception_name: Optional[str] = None
    additional_equipment: Optional[FOCRAddEquipmentSchema] = None
    
    class Config:
        from_attributes = True


class FOCR02SignatureSchema(BaseModel):
    signature_base64: str
    
    class Config:
        from_attributes = True


class FOCR02TableRowSchema(BaseModel):
    id: int
    status: str
    equipment_name: str
    employee_name: str
    date_created: date
    
    class Config:
        from_attributes = True


class FOCR02Schema(BaseModel):
    id: Optional[int] = None
    client: Optional[ClientSimpleSchema] = None
    employee: Optional[EmployeeSimpleSchema] = None
    equipment: Optional[EquipmentSimpleSchema] = None
    file_id: Optional[str] = None
    focr_add_equipment: Optional[FOCRAddEquipmentSchema] = None
    reception_name: Optional[str] = None
    date_created: Optional[date] = None
    status: Optional[str] = None
    signature_path: Optional[str] = None
    date_signed: Optional[date] = None
    
    class Config:
        from_attributes = True
