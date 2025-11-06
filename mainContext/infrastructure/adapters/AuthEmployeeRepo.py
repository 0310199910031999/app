from sqlalchemy.orm import Session
from sqlalchemy import func 
from typing import List, Optional

from mainContext.application.dtos.auth_employee_dto import AuthEmployeeDTO
from mainContext.application.dtos.auth_employee_dto import EmployeeAuthResponseDTO
from mainContext.application.ports.AuthEmployeeRepo import AuthEmployeeRepo
from mainContext.infrastructure.models import Employees as EmployeeModel

from sqlalchemy.exc import SQLAlchemyError


class AuthEmployeeRepoImpl(AuthEmployeeRepo):
    def __init__(self, db: Session):
        self.db = db

    def auth_employee(self, auth_dto: AuthEmployeeDTO) -> EmployeeAuthResponseDTO:
        try:
            employee = self.db.query(EmployeeModel).filter_by(email=auth_dto.email, password=auth_dto.password).first()
            if employee:
                return EmployeeAuthResponseDTO(
                    id=employee.id,
                    name=employee.name,
                    lastname=employee.lastname,
                    email=employee.email,
                    role_name=employee.role.role_name,
                    session_token="" 
                )
            return None
        except SQLAlchemyError as e:
            raise Exception(f"Error authenticating employee: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error authenticating employee: {str(e)}")