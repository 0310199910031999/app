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
    service_description: str


class FOSP01UpdateDTO(BaseModel): 
    hourometer : float 
    observations : str
    reception_name : str
    fosp01_services : List[FOSP01ServiceDTO]


#Signed DTO
class FOSP01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : str
    signature_base64: str
    


#Table Row DTO
class FOSP01TableRowDTO(BaseModel):
    id: int
    file_id : str
    date_created : date
    observations: str
    codigos : List[str]
    employee_name : str
    status : str





