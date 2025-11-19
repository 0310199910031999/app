from dataclasses import dataclass
from mainContext.domain.models.Client import Client
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from datetime import datetime
from typing import Optional

@dataclass
class ClientEquipmentProperty:
    id: int
    property: Optional[str]
    brand: Optional[str]
    model: Optional[str]
    serial_number: Optional[str]

@dataclass
class FOPC02:
    id: int
    client: Client
    employee: Employee
    equipment: Equipment
    property: Optional[ClientEquipmentProperty]
    departure_date: Optional[datetime]
    departure_description: Optional[str]
    return_date: Optional[datetime]
    return_description: Optional[str]
    departure_signature_path: Optional[str]
    departure_employee_signature_path: Optional[str]
    return_signature_path: Optional[str]
    return_employee_signature_path: Optional[str]
    status: Optional[str]
    name_auth_departure: Optional[str]
    name_recipient: Optional[str]
    observations: Optional[str]
    file_id: Optional[str]
    fopc_services_id: Optional[int]
