from abc import ABC, abstractmethod
from typing import List, Optional

from mainContext.application.dtos.auth_employee_dto import EmployeeAuthResponseDTO
from mainContext.application.dtos.auth_employee_dto import AuthEmployeeDTO


class AuthEmployeeRepo(ABC):
    @abstractmethod
    def auth_employee(self, auth_dto: AuthEmployeeDTO) -> EmployeeAuthResponseDTO:
        pass