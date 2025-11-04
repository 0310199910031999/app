from pydantic import BaseModel
from typing import Optional, List

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

class LeasingEquipmentDashDTO(BaseModel):
    id : int
    brand_name : str
    economic_number : str
    client_name : str

class ServiceCodeDashDTO(BaseModel):
    code : str
    count : int

class DashboardDTO(BaseModel):
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
