from typing import Optional
from datetime import datetime
from pydantic import BaseModel


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
