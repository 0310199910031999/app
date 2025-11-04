from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from mainContext.application.dtos.Formats.fo_pc_02_dto import ClientEquipmentPropertyDTO

class FOPP02CreateDTO(BaseModel):
    employee_id : int
    vendor_id : int
    departure_date : date = date.today()
    status : str = "Abierto"
    fopc_id : int

class FOPP02UpdateDTO(BaseModel):
    departure_date : date
    
    materials : List[ClientEquipmentPropertyDTO]

class FOPP02SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()

class FOPP02TableRowDTO(BaseModel):
    id: int
    file_id : str
    date_created : date
    employee_name : str
    status : str