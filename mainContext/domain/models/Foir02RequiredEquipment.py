from dataclasses import dataclass
from typing import Optional

@dataclass
class Foir02RequiredEquipment:
    id: int
    amount: Optional[int]
    unit: Optional[str]
    type: Optional[str]
    name: Optional[str]
