from pydantic import BaseModel
from typing import Optional

class RoleDTO(BaseModel):
    id: int
    role_name: Optional[str] = None

class EmployeeDTO(BaseModel):
    id: int
    role_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    session_token: Optional[str] = None
    role: Optional[RoleDTO] = None

class EmployeeCreateDTO(BaseModel):
    role_id: int
    name: str
    lastname: str
    email: str
    password: str

class EmployeeUpdateDTO(BaseModel):
    role_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    session_token: Optional[str] = None
