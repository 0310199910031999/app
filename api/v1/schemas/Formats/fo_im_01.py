from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from api.v1.schemas.equipment import EquipmentBrandSchema, EquipmentTypeSchema, EquipmentSchema
from api.v1.schemas.client import ClientInfoSchema as ClientSchema
from api.v1.schemas.Formats.fo_im_questions import FOIMQuestionSchema



class RoleSchema(BaseModel):
    id: int
    role_name: str

class EmployeeSchema(BaseModel):
    id : Optional[int] = None
    role : Optional[RoleSchema] = None
    name : Optional[str] = None
    lastname: Optional[str] = None


class FOIM01AnswerSchema(BaseModel):
    id: int
    foim_question : FOIMQuestionSchema
    answer : str
    description : str


class FOIM01Schema(BaseModel):
    id: int
    employee: Optional[EmployeeSchema] = None
    equipment : Optional[EquipmentSchema] = None
    client : Optional[ClientSchema] = None
    hourometer: Optional[float] = None
    observations: Optional[str] = None
    reception_name: Optional[str] = None
    date_created: Optional[date] = None
    status: Optional[str] = None
    signature_path: Optional[str] = None
    date_signed: Optional[date] = None
    rating: Optional[int] = None
    rating_comment: Optional[str] = None
    answers : Optional[List[FOIM01AnswerSchema]] = None

class FOIM01CreateSchema(BaseModel):
    employee_id : int
    equipment_id : int 
    date_created : date = date.today()
    status : str = "Abierto"




#Update Schemas
class FOIM01AnswerSchema(BaseModel):
    foim_question_id : int
    answer : str
    description : Optional[str] = None

class FOIM01UpdateSchema(BaseModel): 
    hourometer : float 
    observations : str
    reception_name : str
    foim01_answers : Optional[List[FOIM01AnswerSchema]] = None


#Signed Schema
class FOIM01SignatureSchema(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : Optional[str] = None
    signature_base64: str


#Table Row Schema
class FOIM01TableRowSchema(BaseModel):
    id: int
    date_created : date
    observations: Optional[str] = None
    employee_name : str
    status : str
