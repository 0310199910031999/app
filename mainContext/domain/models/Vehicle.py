from dataclasses import dataclass
from typing import Optional
from mainContext.domain.models.Employee import Employee  # Adjust the import path as needed

@dataclass
class Vehicle:
    id: int
    name : str
    license_plate : str
    employee : Optional[Employee] = None
    employee_id: Optional[int] = None
    model: Optional[str] = None
    odometer: Optional[float] = None