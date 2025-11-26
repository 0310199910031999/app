from pydantic import BaseModel
from typing import Optional

class FoimQuestionDTO(BaseModel):
    id: int
    function: Optional[str] = None
    question: Optional[str] = None
    target: Optional[str] = None

class FoimQuestionCreateDTO(BaseModel):
    function: str
    question: str
    target: Optional[str] = None

class FoimQuestionUpdateDTO(BaseModel):
    function: Optional[str] = None
    question: Optional[str] = None
    target: Optional[str] = None
