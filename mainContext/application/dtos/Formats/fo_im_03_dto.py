from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class FOIM03AnswerDTO(BaseModel):
    foim_question_id : int
    answer : str
    description : Optional[str] = None
    status : str = "Nuevo"

class FOIM03CreateDTO(BaseModel):
    employee_id : Optional[int] = None
    equipment_id : int 
    app_user_id : int
    date_created : date = date.today()
    status : str = "Nuevo"
    foim03_answers : Optional[List[FOIM03AnswerDTO]] = None


class FOIM03AnswerChangeDTO(BaseModel): 
    id : int
    status : str = "Nuevo"

class FOIM03ChangeStatusDTO(BaseModel):
    foim03_answers : Optional[List[FOIM03AnswerChangeDTO]] = None


class FOIM03TableRowDTO(BaseModel):
    id: int
    date_created : date
    observations: Optional[str] = None
    employee_name : Optional[str] = None
    app_user_name : str
    status : str


class FOIM03ListItemDTO(BaseModel):
    id: int
    client_name: Optional[str] = None
    equipment: Optional[str] = None
    economic_number: Optional[str] = None
    app_user_name: Optional[str] = None
    date_created: Optional[date] = None
    status: Optional[str] = None





