from dataclasses import dataclass
from datetime import date
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Vehicle import Vehicle
from typing import List

@dataclass
class FOIR02RequiredEquipment:
    id : int
    amount : int
    unit : str
    type : str
    name : str

@dataclass
class FOIR02EquipmentChecklist:
    id : int 
    required_equipment : FOIR02RequiredEquipment
    status : bool
    comments : str


@dataclass
class FOIR02:
    id : int
    status : str
    vehicle : Vehicle
    employee : Employee
    supervisor : Employee
    date_route : date
    equipment_checklist : List[FOIR02EquipmentChecklist]