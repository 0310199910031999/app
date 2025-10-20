
from dataclasses import dataclass
from datetime import date, datetime
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.Client import Client
from mainContext.domain.models.File import File
from mainContext.domain.models.Formats.Service import Service
from typing import List

@dataclass
class FOSP01Service:
    id : int
    service : Service
@dataclass
class FOSP01:
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
    rating : int
    rating_comment : str
    fopc_services_id : int
    services : List[FOSP01Service]

