from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class FOBC01CreateDTO(BaseModel):
    employee_id : int
    equipment_id : int 
    date_created : date = date.today()
    status : str = "Abierto"
    battery : Optional[str] = None
    cells_x : Optional[int] = None
    cells_y : Optional[int] = None


class FOBC01AnswerDTO(BaseModel):
    question_id : int
    answer : Optional[str] = None


class FOBC01BatteryCellDTO(BaseModel):
    cell_number : int
    voltage : Optional[float] = None
    density : Optional[float] = None
    status : Optional[str] = None


class FOBC01QuestionDTO(BaseModel):
    id: int
    description: Optional[str] = None
    type: Optional[str] = None


class FOBC01QuestionCreateDTO(BaseModel):
    description: str
    type: Optional[str] = None


class FOBC01QuestionUpdateDTO(BaseModel):
    description: Optional[str] = None
    type: Optional[str] = None

class FOBC01UpdateDTO(BaseModel):
    hourometer : float
    observations : str
    reception_name : str
    employee_id : int
    battery : Optional[str] = None
    cells_x : Optional[int] = None
    cells_y : Optional[int] = None
    fobc01_answers : Optional[List[FOBC01AnswerDTO]] = None
    fobc01_battery_cells : Optional[List[FOBC01BatteryCellDTO]] = None

class FOBC01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : str
    signature_base64: str
    employee_id : int

class FOBC01TableRowDTO(BaseModel):
    id: int
    file_id : Optional[str]
    date_created : date
    observations: Optional[str] = None
    employee_name : Optional[str]
    status : str
