from mainContext.application.ports.AppVersionRepo import AppVersionRepo
from mainContext.application.dtos.app_version_dto import AppVersionDTO, AppVersionCreateDTO, AppVersionUpdateDTO
from mainContext.infrastructure.models import AppVersions as AppVersionModel
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

class AppVersionRepoImpl(AppVersionRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_app_version(self, dto: AppVersionCreateDTO) -> int:
        try:
            model = AppVersionModel(
                version_number=dto.version_number,
                platform=dto.platform
            )

            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)

            if not model.id or model.id <= 0:
                raise Exception("Error al registrar version en la base de datos")

            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear version: {str(e)}")

    def get_app_version_by_id(self, id: int) -> Optional[AppVersionDTO]:
        try:
            model = self.db.query(AppVersionModel).filter_by(id=id).first()

            if not model:
                return None

            return AppVersionDTO(
                id=model.id,
                version_number=model.version_number,
                platform=model.platform
            )
        except Exception as e:
            raise Exception(f"Error al obtener version: {str(e)}")

    def get_all_app_versions(self) -> List[AppVersionDTO]:
        try:
            models = self.db.query(AppVersionModel).all()

            return [
                AppVersionDTO(
                    id=model.id,
                    version_number=model.version_number,
                    platform=model.platform
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener versions: {str(e)}")

    def update_app_version(self, id: int, dto: AppVersionUpdateDTO) -> bool:
        try:
            model = self.db.query(AppVersionModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.version_number is not None:
                model.version_number = dto.version_number
            if dto.platform is not None:
                model.platform = dto.platform

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar version: {str(e)}")

    def delete_app_version(self, id: int) -> bool:
        try:
            model = self.db.query(AppVersionModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar version: {str(e)}")

    def get_latest_version_number(self) -> Optional[float]:
        try:
            result = self.db.query(func.max(AppVersionModel.version_number)).scalar()
            return result
        except Exception as e:
            raise Exception(f"Error al obtener ultima version: {str(e)}")
