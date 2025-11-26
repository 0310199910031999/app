from pydantic import BaseModel
from typing import Optional

class VendorDTO(BaseModel):
    id: int
    name: Optional[str] = None
    rfc: Optional[str] = None
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class VendorCreateDTO(BaseModel):
    name: str
    rfc: Optional[str] = None
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class VendorUpdateDTO(BaseModel):
    name: Optional[str] = None
    rfc: Optional[str] = None
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
