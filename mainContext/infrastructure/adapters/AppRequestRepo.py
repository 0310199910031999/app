import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from mainContext.application.ports.AppRequestRepo import AppRequestRepo
from mainContext.application.dtos.app_request_dto import (
    AppRequestDTO,
    AppRequestCreateDTO,
    AppRequestUpdateDTO,
    AppRequestCloseDTO,
)
from mainContext.infrastructure.models import AppRequests as AppRequestModel


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
            models = self.db.query(AppRequestModel).all()
            return [self._to_dto(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar solicitudes en app: {exc}")

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
