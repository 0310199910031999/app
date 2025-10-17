from pydantic import BaseModel
from datetime import date
from typing import List, Optional

#Create DTO 
class FOSC01CreateDTO(BaseModel):
    equipment_id : int
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"

#Update DTOs
class FOSC01ServiceDTO(BaseModel):
    service_id: int
    diagnose_description: str
    description_service: str
    priority: str

class FOSC01UpdateDTO(BaseModel):
    hourometer : float
    observations : str
    reception_name : str
    fosc01_services : List[FOSC01ServiceDTO]

#Signed DTO
class FOSC01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : str
    signature_base64: str

#Table Row DTO
class FOSC01TableRowDTO(BaseModel):
    id: int
    file_id : str
    date_created : date
    observations: str
    codigos : List[str]
    employee_name : str
    status : str
