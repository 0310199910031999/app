from typing import Optional
from pydantic import BaseModel

from mainContext.application.dtos.spare_part_category_dto import SparePartCategoryDTO


class SparePartDTO(BaseModel):
    id: int
    description: str
    category_id: int
    category: Optional[SparePartCategoryDTO] = None


class SparePartCreateDTO(BaseModel):
    description: str
    category_id: int


class SparePartUpdateDTO(BaseModel):
    description: Optional[str] = None
    category_id: Optional[int] = None
