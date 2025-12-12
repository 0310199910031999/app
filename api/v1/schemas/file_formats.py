from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileFormatSchema(BaseModel):
    """Schema para representar un formato asociado a un file con validación opcional"""
    id: Optional[int] = None
    format: Optional[str] = None
    file_id: Optional[str] = None
    equipment: Optional[str] = None
    date_created: Optional[datetime] = None
    employee: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True
