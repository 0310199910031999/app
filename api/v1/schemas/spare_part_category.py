from typing import Optional
from pydantic import BaseModel


class SparePartCategorySchema(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True


class SparePartCategoryCreateSchema(BaseModel):
    description: str


class SparePartCategoryUpdateSchema(BaseModel):
    description: Optional[str] = None
