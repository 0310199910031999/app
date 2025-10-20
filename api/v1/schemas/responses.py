from pydantic import BaseModel

class ResponseBoolModel(BaseModel):
    result : bool

class ResponseIntModel(BaseModel):
    id : int