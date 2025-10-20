from dataclasses import dataclass

@dataclass
class Service:
    id: int
    code : str
    name : str
    description : str
    type : str