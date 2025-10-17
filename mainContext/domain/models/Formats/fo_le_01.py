from dataclasses import dataclass
from datetime import date, datetime
from mainContext.domain.models.Equipment import Equipment  # Adjust the import path as needed
from mainContext.domain.models.Employee import Employee  # Adjust the import path as needed
from mainContext.domain.models.Formats.Service import Service  # Adjust the import path as needed
from mainContext.domain.models.Client import Client
from typing import List


@dataclass
class FOLE01Service:
    id: int
    service : Service
    diagnose_description : str
    description_service : str
    priority: str

@dataclass
class FOLE01:
    id: int
    employee: Employee
    equipment: Equipment
    client : Client
    horometer: float
    technical_action : str
    status: str
    reception_name: str
    signature_path: str
    date_signed: date
    date_created: date
    rating: int
    rating_comment: str
    services : List[FOLE01Service]


    