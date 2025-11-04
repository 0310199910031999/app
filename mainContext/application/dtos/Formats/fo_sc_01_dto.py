from pydantic import BaseModel
from datetime import date
from typing import List, Optional

#Create DTO 
class FOSC01CreateDTO(BaseModel):
    equipment_id : int
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"
    GC : str = None


#Update DTOs
class FOSC01ServiceDTO(BaseModel):
    service_id: int
    service_description: str

class FOSC01UpdateDTO(BaseModel):
    hourometer : float
    observations : str
    reception_name : str
    fosc01_services : Optional[List[FOSC01ServiceDTO]] = None
    evidence_photos_before_base64 : Optional[List[str]] = None
    evidence_photos_after_base64 : Optional[List[str]] = None

#Signed DTO
class FOSC01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : Optional[str] = None
    signature_base64: str

#Table Row DTO
class FOSC01TableRowDTO(BaseModel):
    id: int
    file_id : Optional[str] = None
    date_created : date
    observations: Optional[str] = None
    codes : Optional[List[str]] = None
    employee_name : str
    status : str
