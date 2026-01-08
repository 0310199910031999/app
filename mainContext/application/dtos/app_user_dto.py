from pydantic import BaseModel
from typing import Optional

class ClientDTO(BaseModel):
    id: int
    name: Optional[str] = None
    rfc: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None

class AppUserDTO(BaseModel):
    id: int
    client_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    token_fcm: Optional[str] = None


class AppUserInfoDTO(BaseModel):
    """Lightweight AppUser info for nested responses"""
    id: int
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None

class AppUserCreateDTO(BaseModel):
    client_id: int
    name: str
    lastname: str
    email: str
    password: str
    phone_number: Optional[str] = None
    token_fcm: Optional[str] = None

class AppUserUpdateDTO(BaseModel):
    client_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    token_fcm: Optional[str] = None


class AuthAppUserDTO(BaseModel):
    email: str
    password: str


class AppUserAuthResponseDTO(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    token_fcm: Optional[str] = None
