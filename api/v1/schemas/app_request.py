from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from api.v1.schemas.service import ServiceSchema
from api.v1.schemas.spare_part import SparePartSchema


class AppRequestSchema(BaseModel):
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
    service: Optional[ServiceSchema] = None
    spare_part: Optional[SparePartSchema] = None

    class Config:
        from_attributes = True


class AppRequestCreateSchema(BaseModel):
    client_id: int
    equipment_id: int
    app_user_id: int
    status: str
    service_name: Optional[str] = None
    request_type: Optional[str] = None
    service_id: Optional[int] = None
    spare_part_id: Optional[int] = None


class AppRequestUpdateSchema(BaseModel):
    client_id: Optional[int] = None
    equipment_id: Optional[int] = None
    app_user_id: Optional[int] = None
    status: Optional[str] = None
    service_name: Optional[str] = None
    request_type: Optional[str] = None
    service_id: Optional[int] = None
    spare_part_id: Optional[int] = None


class AppRequestCloseSchema(BaseModel):
    status: Optional[str] = None
    date_closed: Optional[datetime] = None


class AppRequestWithServiceSchema(AppRequestSchema):
    service: Optional[ServiceSchema] = None


class AppRequestWithSparePartSchema(AppRequestSchema):
    spare_part: Optional[SparePartSchema] = None
