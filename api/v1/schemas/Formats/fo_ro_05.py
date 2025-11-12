from pydantic import BaseModel, Field
from datetime import date, time
from typing import List, Optional
from api.v1.schemas.employee import EmployeeSchema



class FORO05CreateSchema(BaseModel): 
    route_date : date = date.today()
    status : str = "Abierto"

class FORO05EmployeeCheck(BaseModel):
    neat : Optional[bool]
    full_uniform : Optional[bool]
    clean_uniform : Optional[bool]
    safty_boots : Optional[bool]
    ddg_id : Optional[bool]
    valid_license : Optional[bool]
    presentation_card : Optional[bool]
    class Config:
        from_attributes = True

class FORO05VehicleCheck(BaseModel):
    checklist : Optional[bool]
    clean_tools : Optional[bool]
    tidy_tools : Optional[bool]
    clean_vehicle : Optional[bool]
    tidy_vehicle : Optional[bool]
    fuel : Optional[bool]
    documents : Optional[bool]
    

class FORO05ServiceSuplie(BaseModel):
    name : str
    status : bool

    

class FORO05Service(BaseModel):
    client_id : Optional[int] 
    equipment_id : Optional[int]
    service_id : Optional[int]
    file_id : Optional[int] = None
    start_time : time
    end_time : time
    equipment : str
    service_suplies : List[FORO05ServiceSuplie] = Field(default_factory=list, alias="foro05_service_suplies")



class FORO05UpdateSchema(BaseModel):
    route_date : Optional[date] = date.today()
    comments : str
    employee_checklist : FORO05EmployeeCheck
    vehicle_checklist : FORO05VehicleCheck
    services : List[FORO05Service]

class FORO05SignatureSchema(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    signature_base64: str
    supervisor : bool = False
    employee : bool = False

class FORO05TableRowSchema(BaseModel):
    id : int
    route_date : Optional[date]
    status : str
    employee_name : str
    supervisor_name : str
    vehicle : str

class VehicleSchema(BaseModel):
    id: int
    name : str
    license_plate : str



class FORO05Schema(BaseModel):
    
    id : Optional[int]
    status : Optional[str]
    vehicle : Optional[VehicleSchema]
    employee : Optional[EmployeeSchema]
    supervisor : Optional[EmployeeSchema]
    route_date : Optional[date]
    comments : Optional[str]
    signature_path_employee : Optional[str]
    signature_path_supervisor : Optional[str]
    services : Optional[List[FORO05Service]]
    vehicle_checklist : Optional[FORO05VehicleCheck]
    employee_checklist : Optional[FORO05EmployeeCheck]


class ServiceSchema(BaseModel):
    id : Optional[int] = None
    code_name : Optional[str] = None

class ClientSchema(BaseModel):
    id : Optional[int] = None
    name : Optional[str] = None

class EquipmentSchema(BaseModel):
    id : Optional[int] = None
    name : Optional[str] = None