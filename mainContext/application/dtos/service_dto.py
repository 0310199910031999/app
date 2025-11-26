from pydantic import BaseModel
from typing import Optional

class ServiceDTO(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None

class ServiceCreateDTO(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    type: Optional[str] = None

class ServiceUpdateDTO(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
