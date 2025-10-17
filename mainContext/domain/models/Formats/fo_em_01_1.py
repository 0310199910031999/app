from dataclasses import dataclass
from datetime import date
from mainContext.domain.models.Client import Client
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.File import File
from typing import List


@dataclass
class FOEM011Material:
    id : int
    amount : int
    um : str
    part_number : str
    description : str

@dataclass
class FOEM011:
    id : int
    employee: Employee
    file: File
    client : Client
    date_created: date
    hourometer: float
    status: str
    reception_name: str
    signature_path: str
    date_signed: date
    materials : List[FOEM011Material]
