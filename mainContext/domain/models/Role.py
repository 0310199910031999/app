from dataclasses import dataclass
from typing import Optional

@dataclass
class Role:
    id: int
    role_name: Optional[str]
