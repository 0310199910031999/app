import os
import sys
import threading
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import settings
from shared.db import SessionLocal
from shared.mobile_notification_service import (
    DocumentPushNotificationPayload,
    MobileNotificationService,
)


def enqueue_document_push_notification(
    *,
    client_id: int | None,
    document_type: str,
    document_id: int | str,
    equipment_id: int | str | None = None,
    file_id: str | None = None,
    title: str | None = None,
    body: str | None = None,
    report_url: str | None = None,
    event: str = "document_ready",
    status: str | None = None,
) -> str | None:
    if not settings.FIREBASE_ENABLED:
        return None

    if client_id is None:
        return None

    payload = DocumentPushNotificationPayload(
        client_id=client_id,
        document_type=document_type,
        document_id=document_id,
        equipment_id=equipment_id,
        file_id=file_id,
        title=title,
        body=body,
        report_url=report_url,
        event=event,
        status=status,
    )

    if settings.NOTIFICATION_QUEUE_DRIVER == "thread":
        worker_thread = threading.Thread(
            target=process_document_push_notification,
            args=(payload.model_dump(mode="json"),),
            name=f"push-{payload.document_type}-{payload.document_id}",
            daemon=True,
        )
        worker_thread.start()
        return worker_thread.name

    try:
        import redis
        from rq import Queue
    except ImportError as exc:
        raise RuntimeError("Debes instalar redis y rq para encolar notificaciones push") from exc

    connection = redis.from_url(settings.REDIS_URL)
    queue = Queue(settings.NOTIFICATION_QUEUE_NAME, connection=connection)
    queued_job = queue.enqueue(
        process_document_push_notification,
        payload.model_dump(mode="json"),
        job_timeout="10m",
    )
    return queued_job.id


def process_document_push_notification(payload_data: dict[str, Any]):
    db = SessionLocal()
    try:
        payload = DocumentPushNotificationPayload(**payload_data)
        service = MobileNotificationService(db)
        service.send_document_notification(payload)
    finally:
        db.close()


def start_worker():
    if settings.NOTIFICATION_QUEUE_DRIVER == "thread":
        raise RuntimeError("El worker persistente no aplica cuando NOTIFICATION_QUEUE_DRIVER=thread")

    try:
        import redis
        from rq import SimpleWorker, Worker
    except ImportError as exc:
        raise RuntimeError("Debes instalar redis y rq para ejecutar el worker de notificaciones push") from exc

    connection = redis.from_url(settings.REDIS_URL)
    worker_class = SimpleWorker if os.name == "nt" else Worker
    worker = worker_class([settings.NOTIFICATION_QUEUE_NAME], connection=connection)
    worker.work()


if __name__ == "__main__":
    start_worker()