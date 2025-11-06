from pydantic import BaseModel
from typing import Optional


class ClientCardDTO(BaseModel):
    id : int
    status : str
    name : str
    rfc : str
    contact_person : Optional[str] = None   
    phone_number : Optional[str] = None
    numberClientEquipment : int
    numberDALEquipment : int

class CreateClientDTO(BaseModel):
    name : str
    rfc : str
    address : str
    phone_number : str
    contact_person : str
    email : str
    status : str

