from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ServiceRecordSchema(BaseModel):
    format: str
    id: int
    date_created: Optional[datetime] = None
    employee_name: Optional[str] = None
    status: Optional[str] = None
    rating: Optional[int] = None
    rating_comment: Optional[str] = None
    file_id: Optional[str] = None
    observations: Optional[str] = None
