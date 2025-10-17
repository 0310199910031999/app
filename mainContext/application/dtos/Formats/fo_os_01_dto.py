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
    diagnose_description: str
    description_service: str
    priority: str

class FOOS01UpdateDTO(BaseModel):
    hourometer: float
    observations: str
    reception_name: str
    foos01_services: List[FOOS01ServiceDTO]

class FOOS01SignatureDTO(BaseModel):
    status: str = "Cerrado"
    date_signed: date = date.today()
    rating: int
    rating_comment: str
    signature_base64: str

class FOOS01TableRowDTO(BaseModel):
    id: int
    file_id: str
    date_created: date
    observations: str
    codigos: List[str]
    employee_name: str
    status: str