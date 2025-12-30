from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class DateRangeDTO(BaseModel):
    start_date: date
    end_date: date

class ServiceDashDTO(BaseModel):
    id : int
    serviceName : str
    clientName : str
    equipment : str
    codes : List[str]

class ServiceByDateDashDTO(BaseModel):
    date : str
    number : int

class ClientDashDTO(BaseModel):
    id : int
    name : str
    total_services : int

class LeasingEquipmentDashDTO(BaseModel):
    id : int
    brand_name : str
    economic_number : str
    client_name : str

class ServiceCodeDashDTO(BaseModel):
    code : str
    count : int


class MobileActivityDTO(BaseModel):
    id: int
    format: str
    date: date
    employee_name: str
    status: str


class MobileClientDashboardDTO(BaseModel):
    equipment_count: int
    focr02_count: int
    open_services: int
    closed_services: int
    activity: List[MobileActivityDTO]

class DashboardDTO(BaseModel):
    files : int
    openServices : int
    listOpenServices : List[ServiceDashDTO]
    activeClients : int
    bestClients : List[ClientDashDTO]
    activeEquipment : int 
    servicesByDate : List[ServiceByDateDashDTO]
    operativeRoutes : int
    numberleasingEquipment : int 
    leasingEquipment : List[LeasingEquipmentDashDTO]
    listBestServices : List[ServiceCodeDashDTO]

class BestClientsByDateDTO(BaseModel):
    bestClients: List[ClientDashDTO]

class ServicesByDateRangeDTO(BaseModel):
    servicesByDate: List[ServiceByDateDashDTO]

class BestServicesByDateDTO(BaseModel):
    listBestServices: List[ServiceCodeDashDTO]
