from pydantic import BaseModel


class ServiceSchema(BaseModel):
    id: int
    code : str
    name : str
    description : str
    type : str