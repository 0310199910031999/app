from pydantic import BaseModel

class ClientPanelOverviewSchema(BaseModel):
    name: str
    rfc: str
    contact_person: str
    phone_number: str
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
