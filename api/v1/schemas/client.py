from pydantic import BaseModel
from typing import Optional


class ClientPanelOverviewSchema(BaseModel):
    id : int
    status : str
    name: str
    rfc: str
    contact_person: str
    phone_number: Optional[str] = None
    numberClientEquipment: int
    numberDALEquipment: int

class ClientInfoSchema(BaseModel):
    id: int
    name: str
    rfc: str
    address: str
    contact_person: str
    phone_number: str
    email: str
    status: str


class CreateClientDTO(BaseModel):
    name : Optional[str] = None
    rfc : Optional[str] = None
    address : Optional[str] = None
    phone_number : Optional[str] = None
    contact_person : Optional[str] = None
    email : Optional[str] = None
    status : Optional[str] = None
