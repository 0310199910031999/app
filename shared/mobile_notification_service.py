import logging
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from mainContext.infrastructure.models import AppUsers
from shared.firebase_service import FirebaseService


logger = logging.getLogger("mobile_notification_service")

if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setLevel(logging.INFO)
    _fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [MOBILE_NOTIFICATIONS] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    _handler.setFormatter(_fmt)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


class DocumentPushNotificationPayload(BaseModel):
    client_id: int
    document_type: str
    document_id: int | str
    equipment_id: int | str | None = None
    file_id: str | None = None
    title: str | None = None
    body: str | None = None
    report_url: str | None = None
    event: str = "document_ready"
    status: str | None = None
    screen: str = "document_detail"

    def notification_title(self) -> str:
        return self.title or f"Documento {self.document_type.upper()} disponible"

    def notification_body(self) -> str:
        if self.body:
            return self.body

        parts = [f"Documento {self.document_type.upper()} #{self.document_id} listo para consulta."]
        if self.equipment_id is not None:
            parts.append(f"Equipo #{self.equipment_id}.")
        return " ".join(parts)

    def to_fcm_data(self) -> dict[str, str]:
        return {
            "notification_type": "document_update",
            "screen": self.screen,
            "client_id": str(self.client_id),
            "document_type": self.document_type,
            "document_id": str(self.document_id),
            "equipment_id": "" if self.equipment_id is None else str(self.equipment_id),
            "file_id": self.file_id or "",
            "report_url": self.report_url or "",
            "event": self.event,
            "status": self.status or "",
        }


class MobileNotificationService:
    def __init__(self, db: Session):
        self.db = db

    def _get_client_tokens(self, client_id: int) -> list[str]:
        rows = (
            self.db.query(AppUsers.token_fcm)
            .filter(AppUsers.client_id == client_id)
            .filter(AppUsers.token_fcm.isnot(None))
            .all()
        )

        tokens: list[str] = []
        seen = set()
        for (token_fcm,) in rows:
            token = (token_fcm or "").strip()
            if token and token not in seen:
                seen.add(token)
                tokens.append(token)

        return tokens

    def send_document_notification(
        self,
        payload: DocumentPushNotificationPayload,
    ) -> dict[str, Any]:
        tokens = self._get_client_tokens(payload.client_id)
        if not tokens:
            logger.info(
                "Sin tokens FCM para client_id=%s document_type=%s document_id=%s",
                payload.client_id,
                payload.document_type,
                payload.document_id,
            )

        result = FirebaseService.send_notification_to_tokens(
            tokens=tokens,
            title=payload.notification_title(),
            body=payload.notification_body(),
            data=payload.to_fcm_data(),
        )
        logger.info(
            "Notificación procesada client_id=%s document_type=%s document_id=%s success=%s failed=%s",
            payload.client_id,
            payload.document_type,
            payload.document_id,
            result["success"],
            result["failed"],
        )
        return result