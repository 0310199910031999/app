from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from mainContext.application.dtos.Formats.fo_le_01_dto import FOLE01CreateDTO
from mainContext.application.dtos.Formats.fo_im_01_dto import FOIM01CreateDTO
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01CreateDTO
from mainContext.application.dtos.Formats.fo_sc_01_dto import FOSC01CreateDTO
from mainContext.application.dtos.Formats.fo_os_01_dto import FOOS01CreateDTO
from mainContext.application.dtos.Formats.fo_bc_01_dto import FOBC01CreateDTO
from mainContext.application.dtos.Formats.fo_em_01_dto import FOEM01CreatedDTO

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
