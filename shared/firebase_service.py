import json
import logging
import threading
from typing import Any

import firebase_admin
from firebase_admin import credentials, messaging

from config import settings


logger = logging.getLogger("firebase_service")

if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setLevel(logging.INFO)
    _fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [FIREBASE_SERVICE] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    _handler.setFormatter(_fmt)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


_APP_NAME = "dal-fcm"
_APP_LOCK = threading.Lock()
_FIREBASE_APP = None


class FirebaseService:
    @staticmethod
    def _build_credential():
        if settings.FIREBASE_CREDENTIALS_JSON:
            return credentials.Certificate(json.loads(settings.FIREBASE_CREDENTIALS_JSON))

        if settings.FIREBASE_CREDENTIALS_FILE:
            return credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILE)

        return credentials.ApplicationDefault()

    @classmethod
    def _get_app(cls):
        global _FIREBASE_APP

        if _FIREBASE_APP is not None:
            return _FIREBASE_APP

        with _APP_LOCK:
            if _FIREBASE_APP is not None:
                return _FIREBASE_APP

            try:
                _FIREBASE_APP = firebase_admin.get_app(_APP_NAME)
                return _FIREBASE_APP
            except ValueError:
                pass

            options = {}
            if settings.FIREBASE_PROJECT_ID:
                options["projectId"] = settings.FIREBASE_PROJECT_ID

            credential = cls._build_credential()
            _FIREBASE_APP = firebase_admin.initialize_app(
                credential=credential,
                options=options or None,
                name=_APP_NAME,
            )
            logger.info("Firebase Admin SDK inicializado correctamente.")
            return _FIREBASE_APP

    @staticmethod
    def _sanitize_data(data: dict[str, Any] | None) -> dict[str, str]:
        sanitized: dict[str, str] = {}
        for key, value in (data or {}).items():
            if value is None:
                sanitized[key] = ""
            else:
                sanitized[key] = str(value)
        return sanitized

    @staticmethod
    def _build_android_config() -> messaging.AndroidConfig:
        notification_kwargs: dict[str, str] = {}
        if settings.FIREBASE_ANDROID_CHANNEL_ID:
            notification_kwargs["channel_id"] = settings.FIREBASE_ANDROID_CHANNEL_ID
        if settings.FIREBASE_NOTIFICATION_SOUND:
            notification_kwargs["sound"] = settings.FIREBASE_NOTIFICATION_SOUND

        android_notification = None
        if notification_kwargs:
            android_notification = messaging.AndroidNotification(**notification_kwargs)

        return messaging.AndroidConfig(
            priority="high",
            notification=android_notification,
        )

    @staticmethod
    def _build_apns_config() -> messaging.APNSConfig:
        return messaging.APNSConfig(
            headers={"apns-priority": "10"},
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound=settings.FIREBASE_NOTIFICATION_SOUND or "default",
                    content_available=True,
                )
            ),
        )

    @classmethod
    def send_notification_to_tokens(
        cls,
        tokens: list[str],
        title: str,
        body: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result = {
            "requested": len(tokens),
            "success": 0,
            "failed": 0,
            "message_ids": [],
            "failed_tokens": [],
            "disabled": not settings.FIREBASE_ENABLED,
        }

        if not settings.FIREBASE_ENABLED:
            logger.info("FCM deshabilitado. No se enviarán notificaciones push.")
            return result

        clean_tokens = []
        seen = set()
        for token in tokens:
            normalized = (token or "").strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                clean_tokens.append(normalized)

        result["requested"] = len(clean_tokens)
        if not clean_tokens:
            logger.info("No hay tokens FCM válidos para procesar.")
            return result

        app = cls._get_app()
        message_data = cls._sanitize_data(data)

        for token in clean_tokens:
            try:
                message = messaging.Message(
                    token=token,
                    notification=messaging.Notification(title=title, body=body),
                    data=message_data,
                    android=cls._build_android_config(),
                    apns=cls._build_apns_config(),
                )
                message_id = messaging.send(message, app=app)
                result["success"] += 1
                result["message_ids"].append(message_id)
            except Exception as exc:
                result["failed"] += 1
                result["failed_tokens"].append(token)
                logger.error("Error enviando notificación FCM al token %s: %s", token, exc)

        logger.info(
            "FCM completado. requested=%s success=%s failed=%s",
            result["requested"],
            result["success"],
            result["failed"],
        )
        return result