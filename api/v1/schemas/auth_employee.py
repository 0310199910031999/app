from pydantic import BaseModel
from typing import Optional

class AuthEmployeeDTO(BaseModel):
    email: str
    password: str

class EmployeeAuthResponseDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    role_name: Optional[str] = None
    session_token: Optional[str] = None