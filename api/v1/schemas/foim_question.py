from pydantic import BaseModel
from typing import Optional

class FoimQuestionSchema(BaseModel):
    id: int
    function: Optional[str] = None
    question: Optional[str] = None
    target: Optional[str] = None
    
    class Config:
        from_attributes = True

class FoimQuestionCreateSchema(BaseModel):
    function: str
    question: str
    target: Optional[str] = None

class FoimQuestionUpdateSchema(BaseModel):
    function: Optional[str] = None
    question: Optional[str] = None
    target: Optional[str] = None
