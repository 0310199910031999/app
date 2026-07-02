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


class ServicesByTypeDashSchema(BaseModel):
    service_type: Optional[str]
    total: Optional[int]


class ServicesByEmployeeDashSchema(BaseModel):
    employee_id: Optional[int]
    employee_name: Optional[str]
    employee_lastname: Optional[str]
    employee_full_name: Optional[str]
    total: Optional[int]


class ServicesByTypeAndEmployeeDashSchema(BaseModel):
    service_type: Optional[str]
    employee_id: Optional[int]
    employee_name: Optional[str]
    employee_lastname: Optional[str]
    employee_full_name: Optional[str]
    total: Optional[int]


class ServiceByDateAndEmployeeDashSchema(BaseModel):
    date: Optional[str]
    service_type: Optional[str]
    employee_id: Optional[int]
    employee_name: Optional[str]
    employee_lastname: Optional[str]
    employee_full_name: Optional[str]
    total: Optional[int]

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


class RatingSummarySchema(BaseModel):
    rating_1: int
    rating_2: int
    rating_3: int


class MobileActivitySchema(BaseModel):
    id: int
    format: str
    date: date
    employee_name: str
    status: str
    equipment_id: Optional[int]


class MobileClientDashboardSchema(BaseModel):
    equipment_count: int
    focr02_count: int
    open_services: int
    closed_services: int
    activity: List[MobileActivitySchema]
    services_last_30_days: List[ServiceByDateDashSchema]
    rating_summary: RatingSummarySchema

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
    totalServices: int
    servicesByDate: List[ServiceByDateAndEmployeeDashSchema]
    totalsByServiceType: List[ServicesByTypeDashSchema]
    totalsByEmployee: List[ServicesByEmployeeDashSchema]
    totalsByServiceTypeAndEmployee: List[ServicesByTypeAndEmployeeDashSchema]

class BestServicesByDateSchema(BaseModel):
    listBestServices: List[ServiceCodeDashSchema]


class SearchByIdSchema(BaseModel):
    id: Optional[int]
    format: Optional[str]
    format_display: Optional[str]


class SearchByIdResultSchema(BaseModel):
    results: List[SearchByIdSchema]


class SearchByIdRequestSchema(BaseModel):
    record_id: Optional[int] = None
    file_id: Optional[str] = None
    format: Optional[str] = None


class TechnicianRatingServiceSchema(BaseModel):
    id: Optional[int]
    format: Optional[str]
    format_display: Optional[str]
    rating: Optional[int]
    date: Optional[date]


class TechnicianRatingSchema(BaseModel):
    employee_id: Optional[int]
    employee_name: Optional[str]
    employee_lastname: Optional[str]
    employee_full_name: Optional[str]
    rating_1: Optional[int]
    rating_2: Optional[int]
    rating_3: Optional[int]
    total: Optional[int]
    services: List[TechnicianRatingServiceSchema]


class TechnicianRatingsRequestSchema(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TechnicianRatingsResultSchema(BaseModel):
    ratingsByTechnician: List[TechnicianRatingSchema]
    totals: RatingSummarySchema
    totalTechnicians: int
