from dataclasses import dataclass
from mainContext.domain.models.Client import Client
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from datetime import date

@dataclass
class ClientEquipmentProperty:
    id : int
    equipment : str
    brand : str
    model : str
    serial_number : str
    hourometer : float
    doh : float

@dataclass
class FOPC02:
    id : int
    client : Client
    employee : Employee
    equipment : Equipment
    property : ClientEquipmentProperty
    departure_date : date
    departure_description : str
    return_date : date
    return_description : str
    exit_signature_path : str
    exit_employee_signature_path : str
    return_signature_path : str
    return_employee_signature_path : str
    status : str
    name_auth_departure : str
    name_recipient : str
    observations : str
    fopc_services_id : int
