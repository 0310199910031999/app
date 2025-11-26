from mainContext.application.ports.EmployeeRepo import EmployeeRepo
from mainContext.application.dtos.employee_dto import EmployeeDTO, EmployeeCreateDTO, EmployeeUpdateDTO
from typing import List, Optional

class CreateEmployee:
    def __init__(self, repo: EmployeeRepo):
        self.repo = repo
    
    def execute(self, dto: EmployeeCreateDTO) -> int:
        return self.repo.create_employee(dto)

class GetEmployeeById:
    def __init__(self, repo: EmployeeRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[EmployeeDTO]:
        return self.repo.get_employee_by_id(id)

class GetAllEmployees:
    def __init__(self, repo: EmployeeRepo):
        self.repo = repo
    
    def execute(self) -> List[EmployeeDTO]:
        return self.repo.get_all_employees()

class UpdateEmployee:
    def __init__(self, repo: EmployeeRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: EmployeeUpdateDTO) -> bool:
        return self.repo.update_employee(id, dto)

class DeleteEmployee:
    def __init__(self, repo: EmployeeRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_employee(id)
