from typing import Optional
from pydantic import BaseModel

from api.v1.schemas.spare_part_category import SparePartCategorySchema


class SparePartSchema(BaseModel):
    id: int
    description: str
    category_id: int
    category: Optional[SparePartCategorySchema] = None

    class Config:
        from_attributes = True


class SparePartCreateSchema(BaseModel):
    description: str
    category_id: int


class SparePartUpdateSchema(BaseModel):
    description: Optional[str] = None
    category_id: Optional[int] = None
