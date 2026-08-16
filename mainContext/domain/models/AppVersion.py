from dataclasses import dataclass
from typing import Optional

@dataclass
class AppVersion:
    id: int
    version_number: Optional[float]
    platform: Optional[str]
