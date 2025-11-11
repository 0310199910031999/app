from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class FORO05CreateDTO(BaseModel): 
    route_date : date = date.today()
    status : str = "Abierto"

class FORO05EmployeeCheck(BaseModel):
    neat : bool
    full_uniform : bool
    clean_uniform : bool
    safty_boots : bool
    ddg_id : bool
    valid_license : bool
    presentation_card : bool

class FORO05VehicleCheck(BaseModel):
    checklist : bool
    clean_tools : bool
    tidy_tools : bool
    clean_vehicle : bool
    tidy_vehicle : bool
    fuel : bool
    documents : bool

class FORO05ServiceSuplie(BaseModel):
    name : str
    status : bool

class FORO05Service(BaseModel):
    client_id : int
    equipment_id : int
    service_id : int
    file_id : int
    start_time : str
    end_time : str
    equipment : str
    service_suplies : List[FORO05ServiceSuplie]

class FORO05UpdateDTO(BaseModel):
    route_date : date
    comments : str
    employee_checklist : FORO05EmployeeCheck
    vehicle_checklist : FORO05VehicleCheck
    services : List[FORO05Service]

class FORO05SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    signature_base64: str
    supervisor : bool = False
    employee : bool = False

class FORO05TableRowDTO(BaseModel):
    id : int
    route_date : Optional[date]
    status : str
    employee_name : str
    supervisor_name : str
    vehicle : str
