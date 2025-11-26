from mainContext.application.ports.ServiceRepo import ServiceRepo
from mainContext.application.dtos.service_dto import ServiceDTO, ServiceCreateDTO, ServiceUpdateDTO
from mainContext.infrastructure.models import Services as ServiceModel
from typing import List, Optional
from sqlalchemy.orm import Session

class ServiceRepoImpl(ServiceRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_service(self, dto: ServiceCreateDTO) -> int:
        try:
            model = ServiceModel(
                code=dto.code,
                name=dto.name,
                description=dto.description,
                type=dto.type
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar servicio en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear servicio: {str(e)}")

    def get_service_by_id(self, id: int) -> Optional[ServiceDTO]:
        try:
            model = self.db.query(ServiceModel).filter_by(id=id).first()
            
            if not model:
                return None
            
            return ServiceDTO(
                id=model.id,
                code=model.code,
                name=model.name,
                description=model.description,
                type=model.type
            )
        except Exception as e:
            raise Exception(f"Error al obtener servicio: {str(e)}")

    def get_all_services(self) -> List[ServiceDTO]:
        try:
            models = self.db.query(ServiceModel).all()
            
            return [
                ServiceDTO(
                    id=model.id,
                    code=model.code,
                    name=model.name,
                    description=model.description,
                    type=model.type
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener servicios: {str(e)}")

    def update_service(self, id: int, dto: ServiceUpdateDTO) -> bool:
        try:
            model = self.db.query(ServiceModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.code is not None:
                model.code = dto.code
            if dto.name is not None:
                model.name = dto.name
            if dto.description is not None:
                model.description = dto.description
            if dto.type is not None:
                model.type = dto.type

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar servicio: {str(e)}")

    def delete_service(self, id: int) -> bool:
        try:
            model = self.db.query(ServiceModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar servicio: {str(e)}")
