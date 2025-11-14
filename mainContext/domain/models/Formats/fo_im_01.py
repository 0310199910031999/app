from dataclasses import dataclass

from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.Client import Client
from mainContext.domain.models.Formats.fo_im_questions import FOIMQuestion
from datetime import date
from typing import List, Optional

@dataclass
class FOIM01Answer:
    id: int
    foim_question : FOIMQuestion
    answer : str
    description : str

@dataclass
class FOIM01:
    id: int
    employee: Employee
    equipment : Equipment
    client : Client
    hourometer: float
    observations: str
    reception_name: str
    date_created: date
    status: str
    signature_path: str
    date_signed: date
    rating: int
    rating_comment: str
    answers : List[FOIM01Answer]


