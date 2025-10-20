from dataclasses import dataclass
from datetime import date
from mainContext.domain.models.AppUser import AppUser
from mainContext.domain.models.Employee import Employee
from mainContext.domain.models.Equipment import Equipment
from mainContext.domain.models.Client import Client
from mainContext.domain.models.Formats.fo_im_questions import FOIMQuestion
from typing import List

@dataclass
class FOIM03Answer:
    id : int
    foim_question : FOIMQuestion
    answer : str
    description : str
    status : str

@dataclass
class FOIM03: 
    id : int
    app_user : AppUser
    employee : Employee
    equipment : Equipment
    client : Client
    date_created : date
    status : str
    answers : List[FOIM03Answer]


