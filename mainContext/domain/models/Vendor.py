from dataclasses import dataclass
from typing import Optional

@dataclass
class Vendor:
    id: int
    name: Optional[str]
    rfc: Optional[str]
    contact_person: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
