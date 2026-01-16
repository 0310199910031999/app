from pydantic import BaseModel
from typing import Optional, List
from api.v1.schemas.employee import EmployeeSchema


class VehicleCreateSchema(BaseModel):
    name: str
    license_plate: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None
    employee_id: Optional[int] = None


class VehicleUpdateSchema(BaseModel):
    name: Optional[str] = None
    license_plate: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None
    employee_id: Optional[int] = None


class VehicleSchema(BaseModel):
    id: int
    name: str
    license_plate: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None
    employee_id: Optional[int] = None
    employee: Optional[EmployeeSchema] = None

    class Config:
        from_attributes = True


class VehicleTableRowSchema(BaseModel):
    id: int
    name: str
    license_plate: Optional[str] = None
    model: Optional[str] = None
    odometer: Optional[float] = None
    employee_name: Optional[str] = None


class VehicleListSchema(BaseModel):
    vehicles: List[VehicleSchema]
