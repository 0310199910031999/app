from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from api.v1.schemas.service import ServiceSchema
from api.v1.schemas.spare_part import SparePartSchema


class ClientInfoSchema(BaseModel):
    id: int
    name: Optional[str] = None
    rfc: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True


class EquipmentInfoSchema(BaseModel):
    id: int
    model: Optional[str] = None
    serial_number: Optional[str] = None
    economic_number: Optional[str] = None
    brand_name: Optional[str] = None

    class Config:
        from_attributes = True


class AppUserInfoSchema(BaseModel):
    id: int
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True


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
    client: Optional[ClientInfoSchema] = None
    equipment: Optional[EquipmentInfoSchema] = None
    app_user: Optional[AppUserInfoSchema] = None

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


class AppRequestStatusSchema(BaseModel):
    status: str


class AppRequestWithServiceSchema(AppRequestSchema):
    service: Optional[ServiceSchema] = None


class AppRequestWithSparePartSchema(AppRequestSchema):
    spare_part: Optional[SparePartSchema] = None
