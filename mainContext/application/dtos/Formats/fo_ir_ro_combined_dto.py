from pydantic import BaseModel
from datetime import date
from typing import Optional


class CreateFOIRROCombinedDTO(BaseModel):
    """
    DTO para crear tanto un FOIR02 como un FORO05 simultáneamente.
    Ambos compartirán el mismo vehicle_id, employee_id, supervisor_id y route_date.
    """
    vehicle_id: int
    employee_id: int
    supervisor_id: int
    route_date: date = date.today()
    status: str = "Abierto"


class FOIRROCombinedResponse(BaseModel):
    """
    Respuesta que contiene los IDs de ambos registros creados.
    """
    foir02_id: int
    foro05_id: int
    vehicle_id: int
    route_date: date
    status: str


class VehicleDTO(BaseModel):
    """
    DTO para representar un vehículo.
    """
    id: int
    name: str
    license_plate: Optional[str] = None
    employee_id: Optional[int] = None


class EmployeeDTO(BaseModel):
    """
    DTO para representar un empleado.
    """
    id: int
    role_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
