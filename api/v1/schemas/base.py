from datetime import datetime, time, timezone
from typing import Any
from pydantic import BaseModel, field_validator


class BaseResponseSchema(BaseModel):
    @field_validator('*', mode='before')
    @classmethod
    def normalize_datetime(cls, value: Any) -> Any:
        if isinstance(value, datetime):
            if value.time() == time(0, 0, 0):
                return value
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
        return value

    class Config:
        from_attributes = True
