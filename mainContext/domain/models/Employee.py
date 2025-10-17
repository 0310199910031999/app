from dataclasses import dataclass


@dataclass
class Role:
    id: int
    role_name: str



@dataclass
class Employee:
    id : int
    role : Role
    name : str
    lastname: str
    email: str
    password: str
    session_token: str
