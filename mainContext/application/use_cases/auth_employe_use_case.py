from typing import List 
from mainContext.application.dtos.auth_employee_dto import EmployeeAuthResponseDTO
from mainContext.application.dtos.auth_employee_dto import AuthEmployeeDTO
from mainContext.application.ports.AuthEmployeeRepo import AuthEmployeeRepo

class AuthEmployee:
    def __init__(self, auth_employee_repo: AuthEmployeeRepo):
        self.auth_employee_repo = auth_employee_repo

    def execute(self, auth_dto: AuthEmployeeDTO) -> EmployeeAuthResponseDTO:
        return self.auth_employee_repo.auth_employee(auth_dto)