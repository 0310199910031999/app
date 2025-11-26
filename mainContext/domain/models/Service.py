from dataclasses import dataclass
from typing import Optional

@dataclass
class Service:
    id: int
    code: Optional[str]
    name: Optional[str]
    description: Optional[str]
    type: Optional[str]
