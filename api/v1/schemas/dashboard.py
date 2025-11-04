from pydantic import BaseModel
from typing import Optional, List


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

class LeasingEquipmentDashSchema(BaseModel):
    id : Optional[int]
    brand_name : Optional[str]
    economic_number : Optional[str]
    client_name : Optional[str]

class ServiceCodeDashSchema(BaseModel):
    code : Optional[str]
    count : Optional[int]

class DashboardSchema(BaseModel):
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
