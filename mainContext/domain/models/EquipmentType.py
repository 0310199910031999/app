from dataclasses import dataclass
from typing import Optional

@dataclass
class EquipmentType:
    id: int
    name: Optional[str]
