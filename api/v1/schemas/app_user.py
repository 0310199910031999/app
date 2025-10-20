from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from api.v1.schemas.client import ClientInfoSchema as ClientSchema


class AppUserSchema(BaseModel):
    id: int
    client: ClientSchema
    name : str
    lastname: str
    email: str
    password: str
    phone_number: str
    token_fcm: str