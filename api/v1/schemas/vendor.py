from pydantic import BaseModel
from typing import Optional

class VendorSchema(BaseModel):
    id: int
    name: Optional[str] = None
    rfc: Optional[str] = None
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        from_attributes = True
