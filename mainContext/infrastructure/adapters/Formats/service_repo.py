from mainContext.domain.models.Formats.Service import Service

from mainContext.application.dtos.Formats.service_dto import ServiceCreateDTO, ServiceUpdateDTO, ServiceTableRowDTO, ServicesFormatList
from mainContext.application.ports.Formats.service_repo import ServiceRepo

from mainContext.infrastructure.models import Services as ServiceModel

from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

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
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al crear el servicio: {str(e)}")

    def get_service_by_id(self, id: int) -> Service:
        model = self.db.query(ServiceModel).filter_by(id=id).first()
        return Service(
            id=model.id,
            code=model.code,
            name=model.name,
            description=model.description,
            type=model.type
        ) if model else None

    def delete_service(self, id: int) -> bool:
        model = self.db.query(ServiceModel).filter_by(id=id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def update_service(self, id: int, dto: ServiceUpdateDTO) -> bool:
        try:
            model = self.db.query(ServiceModel).filter_by(id=id).first()
            if not model:
                return False
            if dto.code:
                model.code = dto.code
            if dto.name:
                model.name = dto.name
            if dto.description:
                model.description = dto.description
            if dto.type:
                model.type = dto.type
            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            return False

    def get_list_services(self) -> List[ServiceTableRowDTO]:
        models = self.db.query(ServiceModel).order_by(desc(ServiceModel.id)).all()
        return [
            ServiceTableRowDTO(
                id=model.id,
                code=model.code,
                name=model.name,
                description=model.description,
                type=model.type
            )
            for model in models
        ]

    
    def get_sp_services(self) -> List[ServicesFormatList]:
        models = self.db.query(ServiceModel).filter_by(type="Preventivo").order_by(desc(ServiceModel.id)).all()
        return [
            ServicesFormatList(
                id=model.id,
                code=model.code,
                name=model.name,
                description=model.description,
                type=model.type
            )
            for model in models
        ]

    def get_sc_services(self) -> List[ServicesFormatList]:
        models = self.db.query(ServiceModel).filter_by(type="Correctivo").order_by(desc(ServiceModel.id)).all()
        return [
            ServicesFormatList(
                id=model.id,
                code=model.code,
                name=model.name,
                description=model.description,
                type=model.type
            )
            for model in models
        ]

    def get_os_services(self) -> List[ServicesFormatList]:
        models = self.db.query(ServiceModel).filter_by(type="Otros Servicios").order_by(desc(ServiceModel.id)).all()
        return [
            ServicesFormatList(
                id=model.id,
                code=model.code,
                name=model.name,
                description=model.description,
                type=model.type
            )
            for model in models
        ]
            