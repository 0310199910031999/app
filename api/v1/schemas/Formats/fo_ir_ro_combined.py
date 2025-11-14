from pydantic import BaseModel
from datetime import date
from typing import Optional


class CreateFOIRROCombinedSchema(BaseModel):
    """
    Schema para crear tanto un FOIR02 como un FORO05 simultáneamente.
    """
    vehicle_id: int
    employee_id: int
    supervisor_id: int
    route_date: date = date.today()
    status: str = "Abierto"
    
    class Config:
        from_attributes = True


class FOIRROCombinedResponseSchema(BaseModel):
    """
    Schema de respuesta con los IDs de ambos registros creados.
    """
    foir02_id: int
    foro05_id: int
    vehicle_id: int
    route_date: date
    status: str
    
    class Config:
        from_attributes = True


class VehicleSchema(BaseModel):
    """
    Schema para representar un vehículo.
    """
    id: int
    name: str
    license_plate: Optional[str] = None
    employee_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class EmployeeSchema(BaseModel):
    """
    Schema para representar un empleado.
    """
    id: int
    role_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        from_attributes = True
