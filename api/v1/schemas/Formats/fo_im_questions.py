from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class FOIMQuestionSchema(BaseModel):
    id: int
    function : str
    question : str
    target : str