from pydantic import BaseModel
from typing import Optional

class RoleDTO(BaseModel):
    id: int
    role_name: Optional[str] = None

class RoleCreateDTO(BaseModel):
    role_name: str

class RoleUpdateDTO(BaseModel):
    role_name: Optional[str] = None
