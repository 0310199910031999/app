from pydantic import BaseModel
from typing import Optional, List

class BrandDTO(BaseModel):
    id : int
    name : str

class TypeDTO(BaseModel):
    id : int
    name : str


class BrandsTypesDTO(BaseModel):
    brands : List[BrandDTO]
    types : List[TypeDTO]
