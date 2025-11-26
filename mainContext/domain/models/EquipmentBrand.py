from dataclasses import dataclass
from typing import Optional

@dataclass
class EquipmentBrand:
    id: int
    name: Optional[str]
    img_path: Optional[str]
