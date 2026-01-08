import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from mainContext.application.ports.AppRequestRepo import AppRequestRepo
from mainContext.application.dtos.app_request_dto import (
    AppRequestDTO,
    AppRequestCreateDTO,
    AppRequestUpdateDTO,
    AppRequestCloseDTO,
    AppRequestStatusDTO,
)
from mainContext.application.dtos.service_dto import ServiceDTO
from mainContext.application.dtos.spare_part_dto import SparePartDTO
from mainContext.application.dtos.spare_part_category_dto import SparePartCategoryDTO
from mainContext.application.dtos.app_user_dto import ClientDTO, AppUserInfoDTO
from mainContext.application.dtos.equipment_dto import EquipmentInfoDTO
from mainContext.infrastructure.models import AppRequests as AppRequestModel
from mainContext.infrastructure.models import SpareParts, Equipment


class AppRequestRepoImpl(AppRequestRepo):
    def __init__(self, db: Session):
        self.db = db

    def _to_dto(self, model: AppRequestModel) -> AppRequestDTO:
        return AppRequestDTO(
            id=model.id,
            client_id=model.client_id,
            equipment_id=model.equipment_id,
            app_user_id=model.app_user_id,
            service_name=model.service_name,
            request_type=model.request_type,
            status=model.status,
            date_created=model.date_created,
            date_closed=model.date_closed,
            service_id=model.service_id,
            spare_part_id=model.spare_part_id,
        )

    def _to_dto_with_service(self, model: AppRequestModel) -> AppRequestDTO:
        service_dto = None
        if model.service is not None:
            service_dto = ServiceDTO(
                id=model.service.id,
                code=model.service.code,
                name=model.service.name,
                description=model.service.description,
                type=model.service.type,
            )
        dto = self._to_dto(model)
        dto.service = service_dto
        return dto

    def _to_dto_with_spare_part(self, model: AppRequestModel) -> AppRequestDTO:
        spare_part_dto = None
        if model.spare_part is not None:
            category_dto = None
            if model.spare_part.category is not None:
                category_dto = SparePartCategoryDTO(
                    id=model.spare_part.category.id,
                    description=model.spare_part.category.description,
                )
            spare_part_dto = SparePartDTO(
                id=model.spare_part.id,
                description=model.spare_part.description,
                category_id=model.spare_part.category_id,
                category=category_dto,
            )
        dto = self._to_dto(model)
        dto.spare_part = spare_part_dto
        return dto

    def _to_dto_with_relations(self, model: AppRequestModel) -> AppRequestDTO:
        """Map model including service, spare part, client, equipment, and app_user when available."""
        dto = self._to_dto(model)

        # Map Client
        if model.client is not None:
            dto.client = ClientDTO(
                id=model.client.id,
                name=model.client.name,
                rfc=model.client.rfc,
                address=model.client.address,
                phone_number=model.client.phone_number,
                contact_person=model.client.contact_person,
                email=model.client.email,
                status=model.client.status,
            )

        # Map Equipment
        if model.equipment is not None:
            brand_name = None
            if model.equipment.brand is not None:
                brand_name = model.equipment.brand.name
            dto.equipment = EquipmentInfoDTO(
                id=model.equipment.id,
                model=model.equipment.model,
                serial_number=model.equipment.serial_number,
                economic_number=model.equipment.economic_number,
                brand_name=brand_name,
            )

        # Map AppUser
        if model.app_user is not None:
            dto.app_user = AppUserInfoDTO(
                id=model.app_user.id,
                name=model.app_user.name,
                lastname=model.app_user.lastname,
                email=model.app_user.email,
            )

        # Map Service
        if model.service is not None:
            dto.service = ServiceDTO(
                id=model.service.id,
                code=model.service.code,
                name=model.service.name,
                description=model.service.description,
                type=model.service.type,
            )

        # Map Spare Part
        if model.spare_part is not None:
            category_dto = None
            if model.spare_part.category is not None:
                category_dto = SparePartCategoryDTO(
                    id=model.spare_part.category.id,
                    description=model.spare_part.category.description,
                )
            dto.spare_part = SparePartDTO(
                id=model.spare_part.id,
                description=model.spare_part.description,
                category_id=model.spare_part.category_id,
                category=category_dto,
            )

        return dto

    def create_app_request(self, dto: AppRequestCreateDTO) -> int:
        try:
            model = AppRequestModel(
                client_id=dto.client_id,
                equipment_id=dto.equipment_id,
                app_user_id=dto.app_user_id,
                service_name=dto.service_name,
                request_type=dto.request_type,
                status=dto.status,
                date_created=datetime.datetime.now(),
                service_id=dto.service_id,
                spare_part_id=dto.spare_part_id,
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model.id
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al crear solicitud en app: {exc}")

    def get_app_request_by_id(self, app_request_id: int) -> Optional[AppRequestDTO]:
        try:
            model = self.db.query(AppRequestModel).filter_by(id=app_request_id).first()
            if not model:
                return None
            return self._to_dto(model)
        except Exception as exc:
            raise Exception(f"Error al obtener solicitud en app: {exc}")

    def get_all_app_requests(self) -> List[AppRequestDTO]:
        try:
            models = (
                self.db.query(AppRequestModel)
                .options(
                    joinedload(AppRequestModel.service),
                    joinedload(AppRequestModel.spare_part).joinedload(SpareParts.category),
                    joinedload(AppRequestModel.client),
                    joinedload(AppRequestModel.equipment).joinedload(Equipment.brand),
                    joinedload(AppRequestModel.app_user),
                )
                .all()
            )
            return [self._to_dto_with_relations(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar solicitudes en app: {exc}")

    def get_app_requests_by_equipment(self, equipment_id: int) -> List[AppRequestDTO]:
        try:
            models = (
                self.db.query(AppRequestModel)
                .options(
                    joinedload(AppRequestModel.service),
                    joinedload(AppRequestModel.spare_part).joinedload(SpareParts.category),
                    joinedload(AppRequestModel.client),
                    joinedload(AppRequestModel.equipment).joinedload(Equipment.brand),
                    joinedload(AppRequestModel.app_user),
                )
                .filter_by(equipment_id=equipment_id)
                .all()
            )
            return [self._to_dto_with_relations(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar solicitudes en app por equipo: {exc}")

    def get_app_requests_by_equipment_with_service(self, equipment_id: int) -> List[AppRequestDTO]:
        try:
            models = (
                self.db.query(AppRequestModel)
                .options(joinedload(AppRequestModel.service))
                .filter_by(equipment_id=equipment_id)
                .all()
            )
            return [self._to_dto_with_service(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar solicitudes en app por equipo con servicio: {exc}")

    def get_app_requests_by_equipment_with_spare_part(self, equipment_id: int) -> List[AppRequestDTO]:
        try:
            models = (
                self.db.query(AppRequestModel)
                .options(joinedload(AppRequestModel.spare_part).joinedload(SpareParts.category))
                .filter_by(equipment_id=equipment_id)
                .all()
            )
            return [self._to_dto_with_spare_part(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar solicitudes en app por equipo con refacción: {exc}")

    def get_app_requests_with_service(self) -> List[AppRequestDTO]:
        try:
            models = (
                self.db.query(AppRequestModel)
                .options(joinedload(AppRequestModel.service))
                .all()
            )
            return [self._to_dto_with_service(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar solicitudes en app con servicio: {exc}")

    def get_app_requests_with_spare_part(self) -> List[AppRequestDTO]:
        try:
            models = (
                self.db.query(AppRequestModel)
                .options(joinedload(AppRequestModel.spare_part).joinedload(SpareParts.category))
                .all()
            )
            return [self._to_dto_with_spare_part(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar solicitudes en app con refacción: {exc}")

    def update_app_request(self, app_request_id: int, dto: AppRequestUpdateDTO) -> bool:
        try:
            model = self.db.query(AppRequestModel).filter_by(id=app_request_id).first()
            if not model:
                return False

            if dto.client_id is not None:
                model.client_id = dto.client_id
            if dto.equipment_id is not None:
                model.equipment_id = dto.equipment_id
            if dto.app_user_id is not None:
                model.app_user_id = dto.app_user_id
            if dto.service_name is not None:
                model.service_name = dto.service_name
            if dto.request_type is not None:
                model.request_type = dto.request_type
            if dto.status is not None:
                model.status = dto.status
            if dto.service_id is not None:
                model.service_id = dto.service_id
            if dto.spare_part_id is not None:
                model.spare_part_id = dto.spare_part_id

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al actualizar solicitud en app: {exc}")

    def close_app_request(self, app_request_id: int, dto: AppRequestCloseDTO) -> bool:
        try:
            model = self.db.query(AppRequestModel).filter_by(id=app_request_id).first()
            if not model:
                return False

            if dto.status is not None:
                model.status = dto.status

            close_ts = dto.date_closed if dto.date_closed is not None else datetime.datetime.utcnow()
            model.date_closed = close_ts

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al cerrar solicitud en app: {exc}")

    def delete_app_request(self, app_request_id: int) -> bool:
        try:
            model = self.db.query(AppRequestModel).filter_by(id=app_request_id).first()
            if not model:
                return False
            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al eliminar solicitud en app: {exc}")

    def update_app_request_status(self, app_request_id: int, dto: AppRequestStatusDTO) -> bool:
        try:
            model = self.db.query(AppRequestModel).filter_by(id=app_request_id).first()
            if not model:
                return False
            model.status = dto.status
            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al actualizar status de solicitud en app: {exc}")
