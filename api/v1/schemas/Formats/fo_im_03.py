from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from api.v1.schemas.equipment import EquipmentSchema
from api.v1.schemas.client import ClientInfoSchema as ClientSchema
from api.v1.schemas.Formats.fo_im_questions import FOIMQuestionSchema

class AppUserSchema(BaseModel):
    id: int
    client: ClientSchema
    name : str
    lastname: str

class RoleSchema(BaseModel):
    id: int
    role_name: str

class EmployeeSchema(BaseModel):
    id : Optional[int] = None
    role : Optional[RoleSchema] = None
    name : Optional[str] = None
    lastname: Optional[str] = None


class FOIM03AnswerSchema(BaseModel):
    id : int
    foim_question : FOIMQuestionSchema
    answer : str
    description : Optional[str] = None
    status : str


class FOIM03Schema(BaseModel): 
    id : int
    app_user : Optional[AppUserSchema] = None
    employee : Optional[EmployeeSchema] = None
    equipment : Optional[EquipmentSchema] = None
    client : Optional[ClientSchema] = None
    date_created : Optional[date] = None
    status : Optional[str] = None
    answers : Optional[List[FOIM03AnswerSchema]] = None

class FOIM03AnswerSchema(BaseModel):
    foim_question_id : int
    answer : str
    description : Optional[str] = None
    status : str = "Nuevo"

class FOIM03CreateSchema(BaseModel):
    employee_id : int
    equipment_id : int 
    app_user_id : int
    date_created : date = date.today()
    status : str = "Nuevo"
    foim03_answers : Optional[List[FOIM03AnswerSchema]] = None


class FOIM03AnswerChangeSchema(BaseModel): 
    id : int
    status : str = "Nuevo"

class FOIM03ChangeStatusSchema(BaseModel):
    foim03_answers : Optional[List[FOIM03AnswerChangeSchema]] = None


class FOIM03TableRowSchema(BaseModel):
    id: int
    date_created : date
    observations: Optional[str] = None
    employee_name : str
    app_user_name : str
    status : str
