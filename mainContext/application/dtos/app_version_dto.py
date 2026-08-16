from pydantic import BaseModel
from typing import Optional

class AppVersionDTO(BaseModel):
    id: int
    version_number: Optional[float] = None
    platform: Optional[str] = None

class AppVersionCreateDTO(BaseModel):
    version_number: float
    platform: Optional[str] = None

class AppVersionUpdateDTO(BaseModel):
    version_number: Optional[float] = None
    platform: Optional[str] = None
