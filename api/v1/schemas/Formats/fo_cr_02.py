from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class EmployeeSimpleSchema(BaseModel):
    id: int
    name: Optional[str] = None
    lastname: Optional[str] = None
    
    class Config:
        from_attributes = True


class EquipmentBrandSchema(BaseModel):
    id: int
    name: Optional[str] = None
    img_path: Optional[str] = None
    
    class Config:
        from_attributes = True


class EquipmentTypeSchema(BaseModel):
    id: int
    name: Optional[str] = None
    
    class Config:
        from_attributes = True


class EquipmentSimpleSchema(BaseModel):
    id: int
    model: Optional[str] = None
    
    class Config:
        from_attributes = True


class EquipmentCompleteSchema(BaseModel):
    id: int
    client_id: Optional[int] = None
    type_id: Optional[int] = None
    brand_id: Optional[int] = None
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
    brand: Optional[EquipmentBrandSchema] = None
    type: Optional[EquipmentTypeSchema] = None
    
    class Config:
        from_attributes = True


class ClientSimpleSchema(BaseModel):
    id: int
    name: Optional[str] = None
    
    class Config:
        from_attributes = True


class ClientCompleteSchema(BaseModel):
    id: int
    name: Optional[str] = None
    rfc: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    
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
    client_name: Optional[str] = None
    file_id: Optional[str] = None
    file_status: Optional[str] = None
    file_folio: Optional[str] = None
    
    class Config:
        from_attributes = True


class FOCR02Schema(BaseModel):
    id: Optional[int] = None
    client: Optional[ClientCompleteSchema] = None
    employee: Optional[EmployeeSimpleSchema] = None
    equipment: Optional[EquipmentCompleteSchema] = None
    file_id: Optional[str] = None
    focr_add_equipment: Optional[FOCRAddEquipmentSchema] = None
    reception_name: Optional[str] = None
    date_created: Optional[date] = None
    status: Optional[str] = None
    signature_path: Optional[str] = None
    date_signed: Optional[date] = None
    
    class Config:
        from_attributes = True
