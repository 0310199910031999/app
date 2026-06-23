from pydantic import BaseModel
from datetime import date, time
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
    client_id : Optional[int] = None
    equipment_id : Optional[int] = None
    service_id : int
    file_id : Optional[str] = None
    start_time : time
    end_time : time
    equipment : Optional[str] = None
    vendor_id : Optional[int] = None
    service_suplies : List[FORO05ServiceSuplie]

class FORO05UpdateDTO(BaseModel):
    route_date : Optional[date] = date.today()
    employee_id : Optional[int] = None
    vehicle_id : Optional[int] = None
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


class FORO05CalendarFilterDTO(BaseModel):
    start_date: date
    end_date: date


class FORO05CalendarRowDTO(BaseModel):
    fecha: date
    cita: Optional[time]
    cliente: Optional[str]
    equipo: Optional[str]
    contacto: Optional[str]
    servicio: Optional[str]
    file: Optional[str]
    tecnico: Optional[str]
    vehiculo: Optional[str]


class FORO05CalendarDayDTO(BaseModel):
    route_date: date
    services: List[FORO05CalendarRowDTO]



class ServiceDTO(BaseModel):
    id : int
    code_name : str

class ClientDTO(BaseModel):
    id : int
    name : str

class EquipmentDTO(BaseModel):
    id : int
    name : str

class VendorDTO(BaseModel):
    id : int
    name : str