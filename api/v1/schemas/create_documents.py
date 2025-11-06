from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class CreateDTO(BaseModel):
    GC : str = None
    fole : bool = False
    foim : bool = False
    fosp : bool = False
    fosc : bool = False
    foos : bool = False
    fobc : bool = False
    foem : bool = False
    employee_id : int
    equipment_id : int
    date_created : date = date.today()
    status : str = "Abierto"