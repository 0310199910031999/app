from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class FOPP02:
    id: int
    vendor_id: Optional[int]
    property_id: Optional[int]
    departure_date: Optional[datetime]
    departure_description: Optional[str]
    delivery_date: Optional[datetime]
    delivery_description: Optional[str]
    departure_signature_path: Optional[str]
    departure_employee_signature_path: Optional[str]
    delivery_signature_path: Optional[str]
    delivery_employee_signature_path: Optional[str]
    observations: Optional[str]
    employee_id: Optional[int]
    status: Optional[str]
    name_auth_departure: Optional[str]
    name_delivery: Optional[str]
    fopc_id: Optional[int]
    file_id: Optional[str]
    date_created: Optional[datetime]
    employee: Optional[object] = None
    fopc: Optional[object] = None
    property: Optional[object] = None
    vendor: Optional[object] = None
