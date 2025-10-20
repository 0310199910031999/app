from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class FOPC02DTO(BaseModel):
    employee_id : int
    equipment_id : int
    departure_date : date = date.today()
    status : str = "Abierto"
    fopc_services_id : int

class ClientEquipmentPropertyDTO(BaseModel):
    equipment : str
    brand : str
    model : str
    serial_number : str 
    hourometer : float 
    doh : float

class FOPC02UpdateDTO(BaseModel):
    departure_date : date
    departure_description : str
    return_date : date
    return_description : str
    name_auth_departure : str
    name_recipient : str
    observations : str
    property : List[ClientEquipmentPropertyDTO]


class FOPC02SignatureExitDTO(BaseModel):
    exit_signature_base64 : str
    exit_employee_signature_base64 : str
    
class FOPC02SignatureReturnDTO(BaseModel):
    return_signature_base64 : str
    return_employee_signature_base64 : str

class FOPC02TableRowDTO(BaseModel):
    id: int
    file_id : str
    date_created : date
    service_id : str
    format_type : str
    status : str

