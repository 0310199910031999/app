from pydantic import BaseModel
from datetime import date
from typing import List, Optional


#Create DTO
class FOSP01CreateDTO(BaseModel):
    employee_id : int
    equipment_id : int 
    date_created : date = date.today()
    status : str = "Abierto"



#Update DTOs
class FOSP01ServiceDTO(BaseModel):
    service_id: int

class FOSP01UpdateDTO(BaseModel): 
    hourometer : float 
    observations : str
    reception_name : str
    fosp01_services : Optional[List[FOSP01ServiceDTO]] = None
    evidence_photos_before_base64 : Optional[List[str]] = None
    evidence_photos_after_base64 : Optional[List[str]] = None


#Signed DTO
class FOSP01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : Optional[str] = None
    signature_base64: str
    


#Table Row DTO
class FOSP01TableRowDTO(BaseModel):
    id: int
    file_id : Optional[str] = None
    date_created : date
    observations: Optional[str] = None
    codes : Optional[List[str]] = None
    employee_name : str
    status : str





