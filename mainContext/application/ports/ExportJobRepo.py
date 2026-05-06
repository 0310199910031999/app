from abc import ABC, abstractmethod
import datetime
from typing import Optional

from mainContext.application.dtos.export_dto import (
    ExportJobCompleteDTO,
    ExportJobCreateDTO,
    ExportJobDTO,
    ExportJobProgressDTO,
)


class ExportJobRepo(ABC):
    @abstractmethod
    def create_job(self, dto: ExportJobCreateDTO) -> str:
        pass

    @abstractmethod
    def get_job_by_id(self, job_id: str) -> Optional[ExportJobDTO]:
        pass

    @abstractmethod
    def update_job_progress(self, job_id: str, dto: ExportJobProgressDTO) -> bool:
        pass

    @abstractmethod
    def complete_job(self, job_id: str, dto: ExportJobCompleteDTO) -> bool:
        pass

    @abstractmethod
    def fail_job(self, job_id: str, error_message: str) -> bool:
        pass

    @abstractmethod
    def get_job_by_token_hash(self, token_hash: str) -> Optional[ExportJobDTO]:
        pass

    @abstractmethod
    def register_download(self, job_id: str) -> bool:
        pass

    @abstractmethod
    def expire_job(self, job_id: str) -> bool:
        pass

    @abstractmethod
    def list_jobs(
        self,
        *,
        client_id: Optional[int] = None,
        equipment_id: Optional[int] = None,
        requested_by_user_id: Optional[int] = None,
        limit: int = 20,
    ):
        pass

    @abstractmethod
    def update_download_access(self, job_id: str, token_hash: str, expires_at: datetime.datetime) -> bool:
        pass
