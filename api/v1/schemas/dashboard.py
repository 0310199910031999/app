from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class DateRangeSchema(BaseModel):
    start_date: date
    end_date: date

class ServiceDashSchema(BaseModel):
    id : Optional[int]
    serviceName : Optional[str]
    clientName : Optional[str]
    equipment : Optional[str]
    codes : Optional[List[str]]

class ServiceByDateDashSchema(BaseModel):
    date : Optional[str]
    number : Optional[int]

class ClientDashSchema(BaseModel):
    id : Optional[int]
    name : Optional[str]
    total_services : Optional[int]

class LeasingEquipmentDashSchema(BaseModel):
    id : Optional[int]
    brand_name : Optional[str]
    economic_number : Optional[str]
    client_name : Optional[str]

class ServiceCodeDashSchema(BaseModel):
    code : Optional[str]
    count : Optional[int]


class MobileActivitySchema(BaseModel):
    id: int
    format: str
    date: date
    employee_name: str
    status: str


class MobileClientDashboardSchema(BaseModel):
    equipment_count: int
    focr02_count: int
    open_services: int
    closed_services: int
    activity: List[MobileActivitySchema]

class DashboardSchema(BaseModel):
    files : Optional[int]
    openServices : Optional[int]
    listOpenServices : Optional[List[ServiceDashSchema]]
    activeClients : Optional[int]
    bestClients : Optional[List[ClientDashSchema]]
    activeEquipment : Optional[int ]
    servicesByDate : Optional[List[ServiceByDateDashSchema]]
    operativeRoutes : Optional[int]
    numberleasingEquipment : Optional[int ]
    leasingEquipment : Optional[List[LeasingEquipmentDashSchema]]
    listBestServices : Optional[List[ServiceCodeDashSchema]]

class BestClientsByDateSchema(BaseModel):
    bestClients: List[ClientDashSchema]

class ServicesByDateRangeSchema(BaseModel):
    servicesByDate: List[ServiceByDateDashSchema]

class BestServicesByDateSchema(BaseModel):
    listBestServices: List[ServiceCodeDashSchema]
