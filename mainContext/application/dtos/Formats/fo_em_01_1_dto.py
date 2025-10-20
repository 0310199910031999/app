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
    description : str

class FOEM011UpdateDTO(BaseModel):
    reception_name : str
    foem01_1_materials : List[FOEM011MaterialDTO]

class FOEM011SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    signature_base64: str
    
class FOEM011TableRowDTO(BaseModel):
    id: int
    file_id : str
    date_created : date
    employee_name : str
    status : str