from dataclasses import dataclass
from datetime import date
from mainContext.domain.models.Client import Client
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.File import File

@dataclass
class FOCRAddEquipment:
    id : int
    equipment : str
    brand : str
    model : str
    serial_number : str
    equipment_type : str
    economic_number : str
    capability : str
    addition : str


@dataclass
class FOCR02:
    id : int
    client : Client
    employee : Employee
    equipment : Equipment
    file : File
    focr_add_equipment : FOCRAddEquipment
    reception_name : str
    date_created : date
    status : str
    date_signed : date