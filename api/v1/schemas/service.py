from pydantic import BaseModel
from typing import Optional

class ServiceSchema(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    
    class Config:
        from_attributes = True

class ServiceCreateSchema(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    type: Optional[str] = None

class ServiceUpdateSchema(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
