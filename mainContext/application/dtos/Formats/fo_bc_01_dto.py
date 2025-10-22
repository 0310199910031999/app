from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class FOBC01CreateDTO(BaseModel):
    employee_id : int
    equipment_id : int 
    date_created : date = date.today()
    status : str = "Abierto"

class FOBC01UpdateDTO(BaseModel):
    hourometer : float
    observations : str
    reception_name : str

class FOBC01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : str
    signature_base64: str

class FOBC01TableRowDTO(BaseModel):
    id: int
    file_id : Optional[str]
    date_created : date
    employee_name : Optional[str]
    status : str
