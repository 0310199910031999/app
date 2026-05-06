import datetime
import hashlib
import secrets
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse

from api.v1.schemas.export import (
    ExportAcceptedSchema,
    ExportDownloadSchema,
    ExportJobItemSchema,
    ExportJobListSchema,
    ExportRequestSchema,
    ExportRetryAcceptedSchema,
    ExportStatusSchema,
)
from mainContext.application.dtos.export_dto import ExportFormatFiltersDTO, ExportJobCreateDTO, ExportRequestDTO
from mainContext.application.use_cases.export_use_cases import GetExportJobByTokenHash, GetExportStatus, InitiateExportJob, ListExportJobs
from mainContext.infrastructure.adapters.ExportJobRepo import ExportJobRepoImpl
from mainContext.infrastructure.dependencies import get_export_job_repo
from shared.export_worker import enqueue_export_job
from mainContext.application.services.export_batch_service import ExportBatchService
from config import settings


ExportRouter = APIRouter(prefix='/exports', tags=['Exports'])


def _job_download_ready(job, now: datetime.datetime | None = None) -> bool:
    current_time = now or datetime.datetime.now()
    return (
        job.status == 'completed'
        and bool(job.zip_path)
        and (job.token_expires_at is None or job.token_expires_at >= current_time)
    )


def _build_download_url(raw_token: str) -> str:
    export_base_url = (settings.EXPORT_BASE_URL or settings.BASE_URL).rstrip('/')
    return f'{export_base_url}/exports/download/{raw_token}'


def _serialize_job(job) -> ExportJobItemSchema:
    now = datetime.datetime.now()
    return ExportJobItemSchema(
        job_id=job.id,
        requested_by_user_id=job.requested_by_user_id,
        client_id=job.client_id,
        equipment_id=job.equipment_id,
        start_date=job.start_date,
        end_date=job.end_date,
        format_filters=job.format_filters,
        status=job.status,
        stage=job.stage,
        progress_pct=job.progress_pct,
        processed_documents=job.processed_documents,
        total_documents=job.total_documents,
        message=ExportBatchService.status_message(job.stage, job.status, job.error_message),
        download_ready=_job_download_ready(job, now),
        expires_at=job.token_expires_at,
        error_message=job.error_message,
        download_count=job.download_count,
        created_at=job.created_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
        updated_at=job.updated_at,
        can_retry=job.status in {'completed', 'failed', 'expired', 'deleted'},
    )


def _create_job_from_existing(source_job, repo: ExportJobRepoImpl) -> str:
    job_id = str(uuid.uuid4())
    create_dto = ExportJobCreateDTO(
        id=job_id,
        requested_by_user_id=source_job.requested_by_user_id,
        client_id=source_job.client_id,
        equipment_id=source_job.equipment_id,
        start_date=source_job.start_date,
        end_date=source_job.end_date,
        format_filters=source_job.format_filters,
    )

    use_case = InitiateExportJob(repo)
    use_case.execute(create_dto)

    try:
        enqueue_export_job(job_id)
    except Exception as e:
        repo.fail_job(job_id, str(e))
        raise HTTPException(status_code=500, detail=f'No se pudo encolar el export job: {str(e)}')

    return job_id


@ExportRouter.post('/', response_model=ExportAcceptedSchema, status_code=status.HTTP_202_ACCEPTED)
def create_export_job(
    payload: ExportRequestSchema,
    repo: ExportJobRepoImpl = Depends(get_export_job_repo),
):
    job_id = str(uuid.uuid4())
    request_dto = ExportRequestDTO(
        client_id=payload.client_id,
        equipment_id=payload.equipment_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        requesting_user_id=payload.requesting_user_id,
        format_filters=ExportFormatFiltersDTO(**payload.format_filters.model_dump()),
    )

    create_dto = ExportJobCreateDTO(
        id=job_id,
        requested_by_user_id=request_dto.requesting_user_id,
        client_id=request_dto.client_id,
        equipment_id=request_dto.equipment_id,
        start_date=request_dto.start_date,
        end_date=request_dto.end_date,
        format_filters=request_dto.format_filters.model_dump(),
    )

    use_case = InitiateExportJob(repo)
    use_case.execute(create_dto)

    try:
        enqueue_export_job(job_id)
    except Exception as e:
        repo.fail_job(job_id, str(e))
        raise HTTPException(status_code=500, detail=f'No se pudo encolar el export job: {str(e)}')

    return ExportAcceptedSchema(
        job_id=job_id,
        status='queued',
        stage='queued',
        message='Exportación encolada correctamente.',
    )


@ExportRouter.get('/', response_model=ExportJobListSchema)
def list_export_jobs(
    client_id: int | None = Query(default=None),
    equipment_id: int | None = Query(default=None),
    requesting_user_id: int | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    repo: ExportJobRepoImpl = Depends(get_export_job_repo),
):
    use_case = ListExportJobs(repo)
    jobs = use_case.execute(
        client_id=client_id,
        equipment_id=equipment_id,
        requested_by_user_id=requesting_user_id,
        limit=limit,
    )
    return ExportJobListSchema(items=[_serialize_job(job) for job in jobs])


@ExportRouter.get('/{job_id}/status', response_model=ExportStatusSchema)
def get_export_status(job_id: str, repo: ExportJobRepoImpl = Depends(get_export_job_repo)):
    use_case = GetExportStatus(repo)
    job = use_case.execute(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Export job not found')

    return ExportStatusSchema(
        job_id=job.id,
        status=job.status,
        stage=job.stage,
        progress_pct=job.progress_pct,
        processed_documents=job.processed_documents,
        total_documents=job.total_documents,
        message=ExportBatchService.status_message(job.stage, job.status, job.error_message),
        download_ready=_job_download_ready(job),
        expires_at=job.token_expires_at,
        download_url=None,
        error_message=job.error_message,
    )


@ExportRouter.post('/{job_id}/download-link', response_model=ExportDownloadSchema)
def create_download_link(job_id: str, repo: ExportJobRepoImpl = Depends(get_export_job_repo)):
    job = repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Export job not found')

    if not job.zip_path:
        raise HTTPException(status_code=404, detail='No ZIP file available for this export job')

    zip_path = Path(job.zip_path)
    if not zip_path.exists():
        repo.expire_job(job.id)
        ExportBatchService.cleanup_job_artifacts(job.zip_path)
        raise HTTPException(status_code=410, detail='Download artifacts are no longer available for this export job')

    now = datetime.datetime.now()
    if job.status == 'expired' or (job.token_expires_at and job.token_expires_at < now):
        repo.expire_job(job.id)
        ExportBatchService.cleanup_job_artifacts(job.zip_path)
        raise HTTPException(status_code=410, detail='Download link has expired')

    if job.status != 'completed':
        raise HTTPException(status_code=409, detail='Export job is not ready for download yet')

    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    expires_at = now + datetime.timedelta(minutes=settings.EXPORT_URL_TTL_MINUTES)
    repo.update_download_access(job.id, token_hash, expires_at)

    return ExportDownloadSchema(
        job_id=job.id,
        expires_at=expires_at,
        download_url=_build_download_url(raw_token),
    )


@ExportRouter.post('/{job_id}/retry', response_model=ExportRetryAcceptedSchema, status_code=status.HTTP_202_ACCEPTED)
def retry_export_job(job_id: str, repo: ExportJobRepoImpl = Depends(get_export_job_repo)):
    source_job = repo.get_job_by_id(job_id)
    if not source_job:
        raise HTTPException(status_code=404, detail='Export job not found')

    new_job_id = _create_job_from_existing(source_job, repo)
    return ExportRetryAcceptedSchema(
        job_id=new_job_id,
        source_job_id=source_job.id,
        status='queued',
        stage='queued',
        message='Exportación reenviada correctamente.',
    )


@ExportRouter.get('/download/{token}')
def download_export(token: str, repo: ExportJobRepoImpl = Depends(get_export_job_repo)):
    token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
    use_case = GetExportJobByTokenHash(repo)
    job = use_case.execute(token_hash)

    if not job:
        raise HTTPException(status_code=404, detail='Export job not found for this token')

    now = datetime.datetime.now()
    if job.token_expires_at and job.token_expires_at < now:
        repo.expire_job(job.id)
        ExportBatchService.cleanup_job_artifacts(job.zip_path)
        raise HTTPException(status_code=410, detail='Download link has expired')

    if not job.zip_path:
        raise HTTPException(status_code=404, detail='No ZIP file available for this export job')

    zip_path = Path(job.zip_path)
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail='ZIP file not found on server')

    repo.register_download(job.id)
    return FileResponse(
        path=str(zip_path),
        media_type='application/zip',
        filename=job.zip_filename or zip_path.name,
    )
