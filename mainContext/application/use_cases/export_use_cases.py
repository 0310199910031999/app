from typing import Optional

from mainContext.application.dtos.export_dto import (
    ExportJobCreateDTO,
    ExportJobDTO,
    ExportJobProgressDTO,
)
from mainContext.application.ports.ExportJobRepo import ExportJobRepo


class InitiateExportJob:
    def __init__(self, repo: ExportJobRepo):
        self.repo = repo

    def execute(self, dto: ExportJobCreateDTO) -> str:
        return self.repo.create_job(dto)


class GetExportStatus:
    def __init__(self, repo: ExportJobRepo):
        self.repo = repo

    def execute(self, job_id: str) -> Optional[ExportJobDTO]:
        return self.repo.get_job_by_id(job_id)


class UpdateExportJobProgress:
    def __init__(self, repo: ExportJobRepo):
        self.repo = repo

    def execute(self, job_id: str, dto: ExportJobProgressDTO) -> bool:
        return self.repo.update_job_progress(job_id, dto)


class GetExportJobByTokenHash:
    def __init__(self, repo: ExportJobRepo):
        self.repo = repo

    def execute(self, token_hash: str) -> Optional[ExportJobDTO]:
        return self.repo.get_job_by_token_hash(token_hash)


class ListExportJobs:
    def __init__(self, repo: ExportJobRepo):
        self.repo = repo

    def execute(
        self,
        *,
        client_id: Optional[int] = None,
        equipment_id: Optional[int] = None,
        requested_by_user_id: Optional[int] = None,
        limit: int = 20,
    ) -> list[ExportJobDTO]:
        return self.repo.list_jobs(
            client_id=client_id,
            equipment_id=equipment_id,
            requested_by_user_id=requested_by_user_id,
            limit=limit,
        )
