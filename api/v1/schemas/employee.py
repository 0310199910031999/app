from pydantic import BaseModel
from typing import Optional


class RoleSchema(BaseModel):
    id: int
    role_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class EmployeeSchema(BaseModel):
    id: int
    role_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    role: Optional[RoleSchema] = None
    
    class Config:
        from_attributes = True

class EmployeeCreateSchema(BaseModel):
    role_id: int
    name: str
    lastname: str
    email: str
    password: str

class EmployeeUpdateSchema(BaseModel):
    role_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    session_token: Optional[str] = None
