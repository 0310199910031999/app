
from pydantic import BaseModel
from datetime import date
from typing import List

class FOLE01CreateDTO(BaseModel):
    equipment_id : int
    employee_id : int
    client_id : int
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
    fole01_services : List[FOLE01ServiceDTO]

class FOLE01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : str
    signature_base64: str

class FOLE01TableRawDTO(BaseModel):
    id : int
    economic_number : str
    date_created : date
    codes : List[str]
    employee_name : str
    status : str