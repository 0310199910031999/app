from pydantic import BaseModel
from datetime import date
from typing import List, Optional


#Create DTO
class ServiceCreateDTO(BaseModel):
    code : str
    name : str
    description : str
    type : str

class ServiceUpdateDTO(BaseModel): 
    code : Optional[str] = None
    name : Optional[str] = None
    description : Optional[str] = None
    type : Optional[str] = None

class ServiceTableRowDTO(BaseModel):
    id : int
    code : str
    name : str
    description : str
    type : str

class ServicesFormatList(BaseModel):
    id : int 
    code : str
    name : str
    description : str
    type : str