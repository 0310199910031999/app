from pydantic import BaseModel
from datetime import date
from typing import List, Optional

from api.v1.schemas.equipment import EquipmentBrandSchema, EquipmentTypeSchema, EquipmentSchema
from api.v1.schemas.client import ClientInfoSchema as ClientSchema


class RoleSchema(BaseModel):
    id: int
    role_name: str

class EmployeeSchema(BaseModel):
    id : Optional[int] = None
    role : Optional[RoleSchema] = None
    name : Optional[str] = None
    lastname: Optional[str] = None

class FileSchema(BaseModel):
    id: str
    folio: Optional[str]


class FOBC01QuestionSchema(BaseModel):
    id: int
    description: Optional[str] = None
    type: Optional[str] = None

    class Config:
        from_attributes = True


class FOBC01AnswerSchema(BaseModel):
    id: int
    fobc01_question: Optional[FOBC01QuestionSchema] = None
    answer: Optional[str] = None

    class Config:
        from_attributes = True


class FOBC01BatteryCellSchema(BaseModel):
    id: int
    cell_number: Optional[int] = None
    voltage: Optional[float] = None
    density: Optional[float] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True

class FOBC01Schema(BaseModel):
    id: int
    employee : Optional[EmployeeSchema] = None
    equipment : Optional[EquipmentSchema] = None
    client : Optional[ClientSchema] = None
    file : Optional[FileSchema] = None
    date_created : Optional[date] = None
    hourometer : Optional[float] = None
    observations : Optional[str] = None
    status : Optional[str] = None
    reception_name : Optional[str] = None
    signature_path : Optional[str] = None
    date_signed : Optional[date] = None
    doh : Optional[float] = None
    rating : Optional[int] = None
    rating_comment : Optional[str] = None
    battery : Optional[str] = None
    cells_x : Optional[int] = None
    cells_y : Optional[int] = None
    answers : Optional[List[FOBC01AnswerSchema]] = None
    battery_cells : Optional[List[FOBC01BatteryCellSchema]] = None

class FOBC01CreateSchema(BaseModel):
    equipment_id : int
    employee_id : int


class FOBC01AnswerInputSchema(BaseModel):
    question_id : int
    answer : Optional[str] = None


class FOBC01BatteryCellInputSchema(BaseModel):
    cell_number : int
    voltage : Optional[float] = None
    density : Optional[float] = None
    status : Optional[str] = None


class FOBC01QuestionCreateSchema(BaseModel):
    description: str
    type: Optional[str] = None


class FOBC01QuestionUpdateSchema(BaseModel):
    description: Optional[str] = None
    type: Optional[str] = None

class FOBC01UpdateSchema(BaseModel):
    hourometer : float
    observations : str
    reception_name : str
    employee_id : int
    battery : Optional[str] = None
    cells_x : Optional[int] = None
    cells_y : Optional[int] = None
    fobc01_answers : Optional[List[FOBC01AnswerInputSchema]] = None
    fobc01_battery_cells : Optional[List[FOBC01BatteryCellInputSchema]] = None



class FOBC01SignatureSchema(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : str
    signature_base64: str
    employee_id: int

class FOBC01TableRowSchema(BaseModel):
    id: int
    file_id : Optional[str] = None
    date_created : date
    observations: Optional[str] = None
    employee_name : Optional[str] = "N/A"
    status : str
    rating : Optional[int] = None
    rating_comment : Optional[str] = None