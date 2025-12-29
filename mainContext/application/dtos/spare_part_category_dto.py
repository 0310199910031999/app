from typing import Optional
from pydantic import BaseModel


class SparePartCategoryDTO(BaseModel):
    id: int
    description: str


class SparePartCategoryCreateDTO(BaseModel):
    description: str


class SparePartCategoryUpdateDTO(BaseModel):
    description: Optional[str] = None
