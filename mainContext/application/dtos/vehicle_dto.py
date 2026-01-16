from pydantic import BaseModel
from typing import Optional, List
from mainContext.domain.models.Employee import Employee


class VehicleCreateDTO(BaseModel):
    name: str
    license_plate: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None
    employee_id: Optional[int] = None


class VehicleUpdateDTO(BaseModel):
    name: Optional[str] = None
    license_plate: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None
    employee_id: Optional[int] = None


class VehicleDTO(BaseModel):
    id: int
    name: str
    license_plate: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None
    employee_id: Optional[int] = None
    employee: Optional[Employee] = None


class VehicleTableRowDTO(BaseModel):
    id: int
    name: str
    license_plate: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None
    employee_name: Optional[str] = None


class VehicleListDTO(BaseModel):
    vehicles: List[VehicleDTO]
