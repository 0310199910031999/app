from pydantic import BaseModel
from typing import Optional


class RoleSchema(BaseModel):
    id: int
    role_name: str



class EmployeeSchema(BaseModel):
    id : Optional[int] = None
    role : Optional[RoleSchema] = None
    name : Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    session_token: Optional[str] = None
