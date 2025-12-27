from pydantic import BaseModel, model_validator
from typing import Optional


class ResponseBoolModel(BaseModel):
    result: bool


class ResponseIntModel(BaseModel):
    id: Optional[int] = None
    result: Optional[int] = None

    @model_validator(mode="after")
    def sync_fields(self):
        value = self.id if self.id is not None else self.result
        if value is None:
            raise ValueError("id or result is required")
        # keep both in sync for downstream consumers
        object.__setattr__(self, "id", value)
        object.__setattr__(self, "result", value)
        return self