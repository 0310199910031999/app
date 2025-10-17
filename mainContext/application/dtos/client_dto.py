from dataclasses import dataclass

@dataclass
class ClientCardDTO:
    name : str
    rfc : str
    contact_person : str   
    phone_number : str
    numberClientEquipment : int
    numberDALEquipment : int

