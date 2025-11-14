from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class CreateFOIR02DTO(BaseModel):
    status : str = "Abierto"
    vehicle_id : int
    date_route : date = date.today()


class FOIR02RequieredEquipment(BaseModel):
    id : int
    amount : int
    unit : str
    type : str
    name : str

class FOIR02EquipmentChecklist(BaseModel):
    required_equipment : FOIR02RequieredEquipment
    status : bool
    comments : str

class UpdateFOIR02DTO(BaseModel):
    employee_id : int
    supervisor_id : int
    equipment_checklist : List[FOIR02EquipmentChecklist]

class FOIR02SignatureDTO(BaseModel):
    status : str = "Cerrado"
    signature_base64 : str
    is_employee : bool = False
    is_supervisor : bool = False


class FOIR02TableRowDTO(BaseModel):
    id : int
    status : str
    vehicle_name : str
    employee_name : str
    supervisor_name : str
    date_route : date

