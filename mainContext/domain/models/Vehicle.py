from dataclasses import dataclass
from mainContext.domain.models.Employee import Employee  # Adjust the import path as needed

@dataclass
class Vehicle:
    id: int
    name : str
    licence_plate : str
    employee : Employee