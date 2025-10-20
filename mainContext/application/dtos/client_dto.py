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

