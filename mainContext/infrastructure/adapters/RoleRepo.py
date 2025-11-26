from mainContext.application.ports.RoleRepo import RoleRepo
from mainContext.application.dtos.role_dto import RoleDTO, RoleCreateDTO, RoleUpdateDTO
from mainContext.infrastructure.models import Roles as RoleModel
from typing import List, Optional
from sqlalchemy.orm import Session

class RoleRepoImpl(RoleRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_role(self, dto: RoleCreateDTO) -> int:
        try:
            model = RoleModel(
                role_name=dto.role_name
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar rol en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear rol: {str(e)}")

    def get_role_by_id(self, id: int) -> Optional[RoleDTO]:
        try:
            model = self.db.query(RoleModel).filter_by(id=id).first()
            
            if not model:
                return None
            
            return RoleDTO(
                id=model.id,
                role_name=model.role_name
            )
        except Exception as e:
            raise Exception(f"Error al obtener rol: {str(e)}")

    def get_all_roles(self) -> List[RoleDTO]:
        try:
            models = self.db.query(RoleModel).all()
            
            return [
                RoleDTO(
                    id=model.id,
                    role_name=model.role_name
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener roles: {str(e)}")

    def update_role(self, id: int, dto: RoleUpdateDTO) -> bool:
        try:
            model = self.db.query(RoleModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.role_name is not None:
                model.role_name = dto.role_name

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar rol: {str(e)}")

    def delete_role(self, id: int) -> bool:
        try:
            model = self.db.query(RoleModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar rol: {str(e)}")
