from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from mainContext.application.dtos.Formats.fo_im_question_dto import FOIMQuestionDTO


#Create DTO
class FOIM01CreateDTO(BaseModel):
    employee_id : int
    equipment_id : int 
    date_created : date = date.today()
    status : str = "Abierto"




#Update DTOs
class FOIM01AnswerDTO(BaseModel):
    foim_question_id : int
    answer : str
    description : Optional[str] = None

class FOIM01UpdateDTO(BaseModel): 
    hourometer : float 
    observations : str
    reception_name : str
    foim01_answers : Optional[List[FOIM01AnswerDTO]] = None


#Signed DTO
class FOIM01SignatureDTO(BaseModel):
    status : str = "Cerrado"
    date_signed : date = date.today()
    rating : int
    rating_comment : Optional[str] = None
    signature_base64: str


#Table Row DTO
class FOIM01TableRowDTO(BaseModel):
    id: int
    date_created : date
    observations: Optional[str] = None
    employee_name : str
    status : str






