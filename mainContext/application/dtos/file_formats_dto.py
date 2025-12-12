from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileFormatDTO(BaseModel):
    """DTO para representar un formato asociado a un file"""
    id: int
    format: str  # Nombre del formato (FO-SP-01, FO-SC-01, etc.)
    file_id: Optional[str] = None
    equipment: Optional[str] = None  # "Marca - Número Económico" o None
    date_created: Optional[datetime] = None
    employee: Optional[str] = None  # "Nombre Apellido"
    status: Optional[str] = None
    
    class Config:
        from_attributes = True
