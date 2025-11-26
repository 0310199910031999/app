from pydantic import BaseModel
from typing import Optional

class RoleSchema(BaseModel):
    id: int
    role_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class RoleCreateSchema(BaseModel):
    role_name: str

class RoleUpdateSchema(BaseModel):
    role_name: Optional[str] = None
