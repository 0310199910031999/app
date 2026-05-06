import os
import sys
import threading
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import settings
from shared.db import SessionLocal


def enqueue_export_job(job_id: str) -> str:
    if settings.EXPORT_QUEUE_DRIVER == 'thread':
        worker_thread = threading.Thread(
            target=process_export_job,
            args=(job_id,),
            name=f'export-job-{job_id}',
            daemon=True,
        )
        worker_thread.start()
        return worker_thread.name

    try:
        import redis
        from rq import Queue
    except ImportError as exc:
        raise RuntimeError('Debes instalar redis y rq para encolar exportaciones') from exc

    connection = redis.from_url(settings.REDIS_URL)
    queue = Queue('exports', connection=connection)
    queued_job = queue.enqueue(process_export_job, job_id, job_timeout='2h')
    return queued_job.id


def process_export_job(job_id: str):
    from mainContext.application.services.export_batch_service import ExportBatchService
    from mainContext.infrastructure.adapters.AppUserRepo import AppUserRepoImpl
    from mainContext.infrastructure.adapters.ExportDocumentCollectorRepo import ExportDocumentCollectorRepoImpl
    from mainContext.infrastructure.adapters.ExportJobRepo import ExportJobRepoImpl

    db = SessionLocal()
    try:
        service = ExportBatchService(
            job_repo=ExportJobRepoImpl(db),
            collector=ExportDocumentCollectorRepoImpl(db),
            app_user_repo=AppUserRepoImpl(db),
        )
        service.process_job(job_id)
    finally:
        db.close()


def start_worker():
    if settings.EXPORT_QUEUE_DRIVER == 'thread':
        raise RuntimeError('El worker persistente no aplica cuando EXPORT_QUEUE_DRIVER=thread')

    try:
        import redis
        from rq import SimpleWorker, Worker
    except ImportError as exc:
        raise RuntimeError('Debes instalar redis y rq para ejecutar el worker de exportaciones') from exc

    connection = redis.from_url(settings.REDIS_URL)
    worker_class = SimpleWorker if os.name == 'nt' else Worker
    worker = worker_class(['exports'], connection=connection)
    worker.work()


if __name__ == '__main__':
    start_worker()
