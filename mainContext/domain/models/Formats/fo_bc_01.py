from dataclasses import dataclass
from datetime import date
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.Client import Client
from mainContext.domain.models.File import File

@dataclass
class FOBC01:
    id : int
    employee : Employee
    equipment : Equipment
    client : Client
    file : File
    date_created : date
    hourometer : float
    observations : str
    status : str
    reception_name : str
    signature_path : str
    date_signed : date
    doh : float
    rating : int
    rating_comment : str