from pydantic import BaseModel
from datetime import date
from typing import List, Optional





class FOIMQuestionDTO(BaseModel):
    id : int
    function : str
    question : str
    target : str