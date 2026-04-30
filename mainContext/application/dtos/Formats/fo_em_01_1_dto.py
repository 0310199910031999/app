from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class FOEM011CreateDTO(BaseModel):
    client_id : int
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"
    
class FOEM011MaterialDTO(BaseModel):
    amount : int 
    um : str
    part_number : str
    description : Optional[str] = None

class FOEM011UpdateDTO(BaseModel):
    hourometer : float
    reception_name : str
    employee_id : int
    observations : Optional[str] = None
    foem01_1_materials : List[FOEM011MaterialDTO]
    evidence_photos_base64 : Optional[List[str]] = None

class FOEM011SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    signature_base64: str
    employee_id : int
    rating : int
    rating_comment : Optional[str] = None
    
class FOEM011TableRowDTO(BaseModel):
    id: int
    file_id : Optional[str] = None
    date_created : date
    employee_name : str
    status : str
    rating : Optional[int] = None
    rating_comment : Optional[str] = None