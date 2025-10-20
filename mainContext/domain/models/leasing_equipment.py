from dataclasses import dataclass
from mainContext.domain.models.Equipment import Equipment
@dataclass
class LeasingEquipment:
    id : int
    equipment : Equipment
    img_path : str
    technical_sheet_path : str
    price : float
    type : str
    status : str