from dataclasses import dataclass
from typing import Optional

@dataclass
class FoimQuestion:
    id: int
    function: Optional[str]
    question: Optional[str]
    target: Optional[str]
