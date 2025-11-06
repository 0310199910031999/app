from pydantic import BaseModel

class AuthEmployeeDTO(BaseModel):
    email: str
    password: str

class EmployeeAuthResponseDTO(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    role_name: str
    session_token: str