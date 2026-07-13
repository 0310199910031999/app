from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.Client import Client
from mainContext.domain.models.File import File


@dataclass
class FOBC01Question:
    id: int
    description: Optional[str]
    type: Optional[str]


@dataclass
class FOBC01Answer:
    id: int
    fobc01_question: Optional[FOBC01Question]
    answer: Optional[str]


@dataclass
class FOBC01BatteryCell:
    id: int
    cell_number: Optional[int]
    voltage: Optional[float]
    density: Optional[float]
    status: Optional[str]

@dataclass
class FOBC01:
    id : int
    employee : Optional[Employee]
    equipment : Optional[Equipment]
    client : Optional[Client]
    file : Optional[File]
    date_created : Optional[date]
    hourometer : Optional[float]
    observations : Optional[str]
    status : Optional[str]
    reception_name : Optional[str]
    signature_path : Optional[str]
    date_signed : Optional[datetime]
    doh : Optional[float]
    rating : Optional[int]
    rating_comment : Optional[str]
    battery : Optional[str]
    cells_x : Optional[int]
    cells_y : Optional[int]
    answers : Optional[List[FOBC01Answer]]
    battery_cells : Optional[List[FOBC01BatteryCell]]