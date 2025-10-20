from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class FOEM01CreatedDTO(BaseModel):
    equipment_id : int
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"

class FOEM01MaterialDTO(BaseModel):
    amount : int 
    um : str
    part_number : str
    description : Optional[str] = None

class FOEM01UpdateDTO(BaseModel):
    hourometer : float
    reception_name : str
    foem01_materials : List[FOEM01MaterialDTO]

class FOEM01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    signature_base64: str

class FOEM01TableRowDTO(BaseModel):
    id: int
    file_id : Optional[str] = None
    date_created : date
    employee_name : str
    status : str