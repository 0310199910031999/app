from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from mainContext.application.dtos.service_dto import ServiceDTO
from mainContext.application.dtos.spare_part_dto import SparePartDTO


class AppRequestDTO(BaseModel):
    id: int
    client_id: int
    equipment_id: int
    app_user_id: int
    service_name: Optional[str] = None
    request_type: Optional[str] = None
    status: str
    date_created: datetime
    date_closed: Optional[datetime] = None
    service_id: Optional[int] = None
    spare_part_id: Optional[int] = None
    service: Optional[ServiceDTO] = None
    spare_part: Optional[SparePartDTO] = None


class AppRequestCreateDTO(BaseModel):
    client_id: int
    equipment_id: int
    app_user_id: int
    status: str
    service_name: Optional[str] = None
    request_type: Optional[str] = None
    service_id: Optional[int] = None
    spare_part_id: Optional[int] = None


class AppRequestUpdateDTO(BaseModel):
    client_id: Optional[int] = None
    equipment_id: Optional[int] = None
    app_user_id: Optional[int] = None
    status: Optional[str] = None
    service_name: Optional[str] = None
    request_type: Optional[str] = None
    service_id: Optional[int] = None
    spare_part_id: Optional[int] = None


class AppRequestCloseDTO(BaseModel):
    status: Optional[str] = None
    date_closed: Optional[datetime] = None
