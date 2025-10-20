from dataclasses import dataclass

@dataclass
class CreateEquipmentDTO:
    client_id: int
    type_id: int
    brand_id: int
    model: str
    mast: str
    serial_number: str
    hourometer: float
    doh: float
    economic_number: str
    capacity: str
    addition: str
    motor: str
    property: str
