from mainContext.application.ports.EmployeeRepo import EmployeeRepo
from mainContext.application.dtos.employee_dto import EmployeeDTO, EmployeeCreateDTO, EmployeeUpdateDTO, RoleDTO
from mainContext.infrastructure.models import Employees as EmployeeModel, Roles as RoleModel
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

class EmployeeRepoImpl(EmployeeRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_employee(self, dto: EmployeeCreateDTO) -> int:
        try:
            model = EmployeeModel(
                role_id=dto.role_id,
                name=dto.name,
                lastname=dto.lastname,
                email=dto.email,
                password=dto.password,
                session_token=None
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar empleado en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear empleado: {str(e)}")

    def get_employee_by_id(self, id: int) -> Optional[EmployeeDTO]:
        try:
            model = (
                self.db.query(EmployeeModel)
                .options(joinedload(EmployeeModel.role))
                .filter_by(id=id)
                .first()
            )
            
            if not model:
                return None
            
            role_dto = None
            if model.role:
                role_dto = RoleDTO(id=model.role.id, role_name=model.role.role_name)
            
            return EmployeeDTO(
                id=model.id,
                role_id=model.role_id,
                name=model.name,
                lastname=model.lastname,
                email=model.email,
                password=model.password,
                session_token=model.session_token,
                role=role_dto
            )
        except Exception as e:
            raise Exception(f"Error al obtener empleado: {str(e)}")

    def get_all_employees(self) -> List[EmployeeDTO]:
        try:
            models = (
                self.db.query(EmployeeModel)
                .options(joinedload(EmployeeModel.role))
                .all()
            )
            
            result = []
            for model in models:
                role_dto = None
                if model.role:
                    role_dto = RoleDTO(id=model.role.id, role_name=model.role.role_name)
                
                result.append(EmployeeDTO(
                    id=model.id,
                    role_id=model.role_id,
                    name=model.name,
                    lastname=model.lastname,
                    email=model.email,
                    password=model.password,
                    session_token=model.session_token,
                    role=role_dto
                ))
            return result
        except Exception as e:
            raise Exception(f"Error al obtener empleados: {str(e)}")

    def update_employee(self, id: int, dto: EmployeeUpdateDTO) -> bool:
        try:
            model = self.db.query(EmployeeModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.role_id is not None:
                model.role_id = dto.role_id
            if dto.name is not None:
                model.name = dto.name
            if dto.lastname is not None:
                model.lastname = dto.lastname
            if dto.email is not None:
                model.email = dto.email
            if dto.password is not None:
                model.password = dto.password
            if dto.session_token is not None:
                model.session_token = dto.session_token

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar empleado: {str(e)}")

    def delete_employee(self, id: int) -> bool:
        try:
            model = self.db.query(EmployeeModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar empleado: {str(e)}")
