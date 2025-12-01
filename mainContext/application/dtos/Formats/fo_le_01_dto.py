
from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class FOLE01CreateDTO(BaseModel):
    equipment_id : int
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"

class FOLE01ServiceDTO(BaseModel):
    service_id: int
    diagnose_description: str
    description_service: str
    priority: str

class FOLE01UpdateDTO(BaseModel):
    hourometer : float
    technical_action : str
    reception_name : str
    fole01_services : Optional[List[FOLE01ServiceDTO]] = None
    evidence_photos_base64 : Optional[List[str]] = None



class FOLE01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : Optional[str] = None
    signature_base64: str

class FOLE01TableRowDTO(BaseModel):
    id : int
    date_created : date
    codes : Optional[List[str]] = None
    employee_name : str
    status : str
    rating : Optional[int] = None
    rating_comment : Optional[str] = None