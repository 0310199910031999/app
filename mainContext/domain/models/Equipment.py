from dataclasses import dataclass


@dataclass(frozen=True)
class EquipmentType:
    id : int
    name : str

@dataclass(frozen=True)
class EquipmentBrand:
    id : int
    name : str
    img_path : str


@dataclass
class Equipment:

    id : int
    client_id : int
    type : EquipmentType
    brand : EquipmentBrand
    model : str
    mast : str
    serial_number : str
    hourometer : float
    doh : float
    economic_number : str
    capacity : str
    addition : str
    motor : str
    property : str
    
