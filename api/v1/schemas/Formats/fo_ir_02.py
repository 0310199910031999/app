from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from api.v1.schemas.employee import EmployeeSchema


class VehicleSchema(BaseModel):
    id: int
    name: str
    license_plate: Optional[str] = None
    
    class Config:
        from_attributes = True


class FOIR02RequiredEquipmentSchema(BaseModel):
    id: int
    amount: int
    unit: str
    type: str
    name: str
    
    class Config:
        from_attributes = True


class FOIR02EquipmentChecklistSchema(BaseModel):
    required_equipment: FOIR02RequiredEquipmentSchema
    status: bool
    comments: Optional[str] = None
    
    class Config:
        from_attributes = True


class FOIR02CreateSchema(BaseModel):
    status: str = "Abierto"
    vehicle_id: int
    date_route: date = date.today()


class FOIR02UpdateSchema(BaseModel):
    employee_id: int
    supervisor_id: int
    equipment_checklist: List[FOIR02EquipmentChecklistSchema]


class FOIR02SignatureSchema(BaseModel):
    status: str = "Cerrado"
    signature_base64: str
    is_employee: bool = False
    is_supervisor: bool = False


class FOIR02TableRowSchema(BaseModel):
    id: int
    status: str
    vehicle_name: str
    employee_name: str
    supervisor_name: str
    date_route: date
    
    class Config:
        from_attributes = True


class FOIR02Schema(BaseModel):
    id: Optional[int] = None
    status: Optional[str] = None
    vehicle: Optional[VehicleSchema] = None
    employee: Optional[EmployeeSchema] = None
    supervisor: Optional[EmployeeSchema] = None
    date_route: Optional[date] = None
    employee_signature_path: Optional[str] = None
    supervisor_signature_path: Optional[str] = None
    equipment_checklist: Optional[List[FOIR02EquipmentChecklistSchema]] = None
    
    class Config:
        from_attributes = True
