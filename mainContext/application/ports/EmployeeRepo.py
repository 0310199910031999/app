from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.employee_dto import EmployeeDTO, EmployeeCreateDTO, EmployeeUpdateDTO

class EmployeeRepo(ABC):
    @abstractmethod
    def create_employee(self, dto: EmployeeCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_employee_by_id(self, id: int) -> Optional[EmployeeDTO]:
        pass
    
    @abstractmethod
    def get_all_employees(self) -> List[EmployeeDTO]:
        pass
    
    @abstractmethod
    def update_employee(self, id: int, dto: EmployeeUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_employee(self, id: int) -> bool:
        pass
