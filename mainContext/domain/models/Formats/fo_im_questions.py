from dataclasses import dataclass

@dataclass
class FOIMQuestion:
    id: int
    function : str
    question : str
    target : str