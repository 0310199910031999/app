from pydantic import BaseModel


class ServiceSchema(BaseModel):
    id: int
    code : str
    name : str
    description : str
    type : str

class ServiceCreateSchema(BaseModel):
    code : str
    name : str
    description : str
    type : str

class ServiceUpdateSchema(BaseModel): 
    code : str
    name : str
    description : str
    type : str

class ServiceTableRowSchema(BaseModel):
    id : int
    code : str
    name : str
    description : str
    type : str

class ServicesFormatListSchema(BaseModel):
    id : int 
    code : str
    name : str
    description : str
    type : str