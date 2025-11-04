from pydantic import BaseModel
from datetime import date
from typing import List, Optional

#Create DTO
class FOOS01CreateDTO(BaseModel):
    equipment_id: int
    employee_id: int
    date_created: date = date.today()
    status: str = "Abierto"

class FOOS01ServiceDTO(BaseModel):
    service_id: int
    service_description: str

class FOOS01UpdateDTO(BaseModel):
    hourometer: float
    observations: str
    reception_name: str
    foos01_services: Optional[List[FOOS01ServiceDTO]] = None
    evidence_photos_before_base64: Optional[List[str]] = None
    evidence_photos_after_base64: Optional[List[str]] = None

#Signed DTO

class FOOS01SignatureDTO(BaseModel):
    status: str = "Cerrado"
    date_signed: date = date.today()
    rating: int
    rating_comment: Optional[str] = None
    signature_base64: str

class FOOS01TableRowDTO(BaseModel):
    id: int
    file_id: Optional[str] = None
    date_created: date
    observations: Optional[str] = None
    codes: Optional[List[str]] = None
    employee_name: str
    status: str