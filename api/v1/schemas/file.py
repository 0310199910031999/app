from pydantic import BaseModel
from typing import List, Optional
from api.v1.schemas.employee import RoleSchema, EmployeeSchema
from api.v1.schemas.equipment import EquipmentBrandSchema, EquipmentTypeSchema, EquipmentSchema
from api.v1.schemas.client import ClientInfoSchema as ClientSchema
from datetime import date, datetime


class FileSchema(BaseModel):
    id: str
    client: ClientSchema
    date_created: datetime
    status: str
    date_closed: Optional[date] = None
    date_invoiced: Optional[date] = None
    folio_invoice: Optional[str] = None
    uuid: Optional[str] = None
    folio: Optional[str]