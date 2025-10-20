from dataclasses import dataclass
from datetime import date
from mainContext.domain.models.Formats.fo_pc_02 import ClientEquipmentProperty
from mainContext.domain.models.Employee import Employee


@dataclass
class Vendor:
    id : int
    name : str
    rfc : str
    contact_person : str
    phone_number : str
    email : str
    address : str

@dataclass
class FOPP01:
    id : int
    vendor : Vendor
    property : ClientEquipmentProperty
    employee : Employee
    departure_date : date
    departure_description : str
    delivery_date : date
    delivery_description : str
    departure_signature_path : str
    departure_employee_signature_path : str
    delivery_signature_path : str
    delivery_employee_signature_path : str
    name_auth_departure : str
    name_delivery : str
    observations : str
    status : str
    fopc_id : int
