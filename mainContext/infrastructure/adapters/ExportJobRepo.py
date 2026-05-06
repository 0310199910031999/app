import datetime
from typing import Optional

from sqlalchemy.orm import Session

from mainContext.application.dtos.export_dto import (
    ExportJobCompleteDTO,
    ExportJobCreateDTO,
    ExportJobDTO,
    ExportJobProgressDTO,
)
from mainContext.application.ports.ExportJobRepo import ExportJobRepo
from mainContext.infrastructure.models import ExportJobs as ExportJobModel


class ExportJobRepoImpl(ExportJobRepo):
    def __init__(self, db: Session):
        self.db = db

    def _model_to_dto(self, model: ExportJobModel) -> ExportJobDTO:
        return ExportJobDTO(
            id=model.id,
            requested_by_user_id=model.requested_by_user_id,
            client_id=model.client_id,
            equipment_id=model.equipment_id,
            status=model.status,
            stage=model.stage,
            progress_pct=model.progress_pct,
            total_documents=model.total_documents,
            processed_documents=model.processed_documents,
            start_date=model.start_date,
            end_date=model.end_date,
            format_filters=model.format_filters or {},
            zip_filename=model.zip_filename,
            zip_path=model.zip_path,
            zip_size_bytes=model.zip_size_bytes,
            download_token_hash=model.download_token_hash,
            token_expires_at=model.token_expires_at,
            download_count=model.download_count,
            last_download_at=model.last_download_at,
            error_message=model.error_message,
            created_at=model.created_at,
            started_at=model.started_at,
            finished_at=model.finished_at,
            updated_at=model.updated_at,
        )

    def create_job(self, dto: ExportJobCreateDTO) -> str:
        try:
            model = ExportJobModel(
                id=dto.id,
                requested_by_user_id=dto.requested_by_user_id,
                client_id=dto.client_id,
                equipment_id=dto.equipment_id,
                start_date=dto.start_date,
                end_date=dto.end_date,
                format_filters=dto.format_filters,
                status=dto.status,
                stage=dto.stage,
                progress_pct=dto.progress_pct,
                total_documents=dto.total_documents,
                processed_documents=dto.processed_documents,
            )
            self.db.add(model)
            self.db.commit()
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f'Error al crear export job: {str(e)}')

    def get_job_by_id(self, job_id: str) -> Optional[ExportJobDTO]:
        try:
            model = self.db.query(ExportJobModel).filter_by(id=job_id).first()
            if not model:
                return None
            return self._model_to_dto(model)
        except Exception as e:
            raise Exception(f'Error al obtener export job: {str(e)}')

    def update_job_progress(self, job_id: str, dto: ExportJobProgressDTO) -> bool:
        try:
            model = self.db.query(ExportJobModel).filter_by(id=job_id).first()
            if not model:
                return False

            model.status = dto.status
            model.stage = dto.stage
            model.progress_pct = dto.progress_pct
            model.processed_documents = dto.processed_documents
            model.total_documents = dto.total_documents
            model.error_message = dto.error_message
            model.started_at = dto.started_at or model.started_at
            model.finished_at = dto.finished_at or model.finished_at
            model.updated_at = datetime.datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f'Error al actualizar export job: {str(e)}')

    def complete_job(self, job_id: str, dto: ExportJobCompleteDTO) -> bool:
        try:
            model = self.db.query(ExportJobModel).filter_by(id=job_id).first()
            if not model:
                return False

            model.status = 'completed'
            model.stage = 'completed'
            model.progress_pct = 100
            model.zip_filename = dto.zip_filename
            model.zip_path = dto.zip_path
            model.zip_size_bytes = dto.zip_size_bytes
            model.download_token_hash = dto.download_token_hash
            model.token_expires_at = dto.token_expires_at
            model.processed_documents = dto.processed_documents
            model.total_documents = dto.total_documents
            model.finished_at = datetime.datetime.now()
            model.updated_at = datetime.datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f'Error al completar export job: {str(e)}')

    def fail_job(self, job_id: str, error_message: str) -> bool:
        try:
            model = self.db.query(ExportJobModel).filter_by(id=job_id).first()
            if not model:
                return False

            model.status = 'failed'
            model.stage = 'failed'
            model.error_message = error_message
            model.finished_at = datetime.datetime.now()
            model.updated_at = datetime.datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f'Error al marcar fallo de export job: {str(e)}')

    def get_job_by_token_hash(self, token_hash: str) -> Optional[ExportJobDTO]:
        try:
            model = self.db.query(ExportJobModel).filter_by(download_token_hash=token_hash).first()
            if not model:
                return None
            return self._model_to_dto(model)
        except Exception as e:
            raise Exception(f'Error al buscar export job por token: {str(e)}')

    def register_download(self, job_id: str) -> bool:
        try:
            model = self.db.query(ExportJobModel).filter_by(id=job_id).first()
            if not model:
                return False

            model.download_count = (model.download_count or 0) + 1
            model.last_download_at = datetime.datetime.now()
            model.updated_at = datetime.datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f'Error al registrar descarga del export job: {str(e)}')

    def expire_job(self, job_id: str) -> bool:
        try:
            model = self.db.query(ExportJobModel).filter_by(id=job_id).first()
            if not model:
                return False

            model.status = 'expired'
            model.stage = 'expired'
            model.updated_at = datetime.datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f'Error al expirar export job: {str(e)}')

    def list_jobs(
        self,
        *,
        client_id: Optional[int] = None,
        equipment_id: Optional[int] = None,
        requested_by_user_id: Optional[int] = None,
        limit: int = 20,
    ) -> list[ExportJobDTO]:
        try:
            query = self.db.query(ExportJobModel)

            if client_id is not None:
                query = query.filter(ExportJobModel.client_id == client_id)
            if equipment_id is not None:
                query = query.filter(ExportJobModel.equipment_id == equipment_id)
            if requested_by_user_id is not None:
                query = query.filter(ExportJobModel.requested_by_user_id == requested_by_user_id)

            models = (
                query.order_by(ExportJobModel.created_at.desc(), ExportJobModel.id.desc())
                .limit(limit)
                .all()
            )
            return [self._model_to_dto(model) for model in models]
        except Exception as e:
            raise Exception(f'Error al listar export jobs: {str(e)}')

    def update_download_access(self, job_id: str, token_hash: str, expires_at: datetime.datetime) -> bool:
        try:
            model = self.db.query(ExportJobModel).filter_by(id=job_id).first()
            if not model:
                return False

            model.download_token_hash = token_hash
            model.token_expires_at = expires_at
            model.updated_at = datetime.datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f'Error al actualizar acceso de descarga del export job: {str(e)}')
