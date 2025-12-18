from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class ClientSchema(BaseModel):
    id: int
    name: Optional[str] = None
    rfc: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True


class AppUserSchema(BaseModel):
    id: int
    client_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    token_fcm: Optional[str] = None    
    class Config:
        from_attributes = True


class AppUserTableRowSchema(BaseModel):
    """Schema simplificado para visualización en tablas"""
    id: int
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    client_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class AppUserCreateSchema(BaseModel):
    client_id: int
    name: str
    lastname: str
    email: str
    password: str
    phone_number: Optional[str] = None
    token_fcm: Optional[str] = None


class AppUserUpdateSchema(BaseModel):
    client_id: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    token_fcm: Optional[str] = None


class AuthAppUserSchema(BaseModel):
    email: str
    password: str


class AppUserAuthResponseSchema(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    token_fcm: Optional[str] = None

    class Config:
        from_attributes = True
