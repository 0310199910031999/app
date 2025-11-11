from dataclasses import dataclass
from mainContext.domain.models.Client import Client
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.File import File
from mainContext.domain.models.Formats.Service import Service
from mainContext.domain.models.Vehicle import Vehicle
from mainContext.domain.models.Employee import Employee
from datetime import time, date
from typing import List

@dataclass
class FORO05ServiceSuplies:
    id : int
    name : str
    status : int


@dataclass
class FORO05Services:
    id : int 
    client : Client
    equipment : Equipment
    service : Service
    file : File
    start_time : time
    end_time : time
    equipment : str
    service_suplies : List[FORO05ServiceSuplies]

@dataclass
class FORO05VehicleChecklist:
    id : int
    checklist : int
    clean_tools : int
    tidy_tools : int
    clean_vehicle : int
    tidy_vehicle : int
    fuel : int
    documents : int


@dataclass
class FORO05EmployeeChecklist:
    id : int
    neat : int
    full_uniform : int
    clean_uniform : int
    safty_boots : int
    ddg_id : int
    valid_license : int
    presentation_card : int

@dataclass
class FORO05:
    id : int
    status : str
    vehicle : Vehicle
    employee : Employee
    supervisor : Employee
    route_date : date
    comments : str
    signature_path_employee : str
    signature_path_supervisor : str
    services : List[FORO05Services]
    vehicle_checklist : FORO05VehicleChecklist
    employee_checklist : FORO05EmployeeChecklist


