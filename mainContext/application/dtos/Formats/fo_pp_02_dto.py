from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional
from mainContext.application.dtos.Formats.fo_pc_02_dto import ClientEquipmentPropertyDTO

class ClientDTO(BaseModel):
    id: int
    name: str
    rfc : Optional[str] = None
    address : Optional[str] = None
    phone_number : Optional[str] = None
    email : Optional[str] = None
    contact_person : Optional[str] = None

class EquipmentTypeDTO(BaseModel):
    id: int
    name: str

class EquipmentBrandDTO(BaseModel):
    id: int
    name: str

class EquipmentDTO(BaseModel):
    model : str
    serial_number : str
    economic_number : str
    type : EquipmentTypeDTO
    brand : EquipmentBrandDTO  
    mast : str
    hourometer : float
    doh : float
    capacity : str
    addition : str
    motor : str
    property : str

class EmployeeDTO(BaseModel):
    id: int
    name: str
    last_name: str
    email: Optional[str] = None
    
class VendorDTO(BaseModel):
    id: int
    name: str
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    rfc: Optional[str] = None

class FOPP02CreateDTO(BaseModel):
    employee_id : int
    date_created : date = date.today()
    status : str = "Abierto"
    fopc_id : int
    property_id : int
    file_id : Optional[str] = None


class FOPP02UpdateDTO(BaseModel):
    departure_date : Optional[date] = None
    departure_description : Optional[str] = None
    delivery_date : Optional[date] = None
    delivery_description : Optional[str] = None
    name_auth_departure : Optional[str] = None
    name_delivery : Optional[str] = None
    observations : Optional[str] = None
    vendor_id : Optional[int] = None

class FOPP02SignatureDTO(BaseModel):
    signature_base64 : str
    is_employee : bool = False # True si es firma de empleado, False si es de cliente
    is_delivery : bool = False # True si es firma de entrega, False si es de salida

class GetFOPP02ByFOPCDTO(BaseModel):
    fopc_id : int

class FOPP02ByFOPCResponseDTO(BaseModel):
    id : int
    date_created : Optional[datetime] = None
    status : Optional[str] = None
    file_id : Optional[str] = None

class FOPP02TableRowDTO(BaseModel):
    id: int
    status: str
    file : str
    equipment_name : str
    employee_name : str
    date_created : datetime