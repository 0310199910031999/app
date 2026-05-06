# Firebase Mobile Notifications

## Objetivo

Se implementó envío de notificaciones push por Firebase Cloud Messaging para la app Flutter.

La notificación se dispara en los mismos eventos donde hoy se manda correo al cliente para documentos cerrados o firmados.

## Arquitectura

- `shared/firebase_service.py`: inicializa Firebase Admin SDK y envía mensajes FCM.
- `shared/mobile_notification_service.py`: resuelve los `token_fcm` de los `AppUsers` por `client_id` y arma el payload.
- `shared/mobile_notification_worker.py`: encola la notificación en modo `thread` o `redis/rq`.

## Configuración requerida

Pegar estas variables en `.env`:

```env
FIREBASE_ENABLED=true
FIREBASE_PROJECT_ID="tu-proyecto-firebase"
FIREBASE_CREDENTIALS_FILE="C:/ruta/a/firebase-service-account.json"
# Alternativa: JSON completo del service account en una sola línea.
FIREBASE_CREDENTIALS_JSON=
FIREBASE_ANDROID_CHANNEL_ID="documents"
FIREBASE_NOTIFICATION_SOUND="default"

NOTIFICATION_QUEUE_DRIVER="thread"
NOTIFICATION_QUEUE_NAME="notifications"
REDIS_URL="redis://localhost:6379/0"
```

Notas:

- Usa `FIREBASE_CREDENTIALS_FILE` o `FIREBASE_CREDENTIALS_JSON`, no ambos.
- Si quieres usar cola real con Redis/RQ, cambia `NOTIFICATION_QUEUE_DRIVER=redis`.
- Si usas `redis`, debes levantar un worker para notificaciones.

## Worker de notificaciones

Solo si `NOTIFICATION_QUEUE_DRIVER=redis`:

```powershell
& "c:/Users/ddgti/Documents/DAL APP/DAL FastApi/app/.venv/Scripts/python.exe" shared/mobile_notification_worker.py
```

## Payload que recibe Flutter

La push usa `notification` + `data`, siguiendo la recomendación de Firebase para mostrar notificación en background y manejar navegación con `data`.

Keys de `data`:

```json
{
  "notification_type": "document_update",
  "screen": "document_detail",
  "client_id": "10",
  "document_type": "foos01",
  "document_id": "123",
  "equipment_id": "456",
  "file_id": "abc-001",
  "report_url": "https://tu-api/foos01/123/reporte",
  "event": "document_signed",
  "status": "Cerrado"
}
```

## Campos clave para Flutter

- `document_type`: tipo de documento.
- `document_id`: id del documento.
- `equipment_id`: id del equipo.
- `file_id`: id del file si existe.
- `report_url`: URL directa del reporte si quieres usarla como fallback.

## Documentos integrados

- `focr02`
- `foem01`
- `foem01_1`
- `foim01`
- `fole01`
- `foos01`
- `fosc01`
- `fosp01`

## Cómo se resuelven destinatarios

La notificación se envía a todos los `AppUsers` del `client_id` del documento que tengan `token_fcm` no nulo ni vacío.

## Contrato backend relevante

Para registrar el token desde Flutter:

```http
PUT /appUsers/{id}/token-fcm
```

Body:

```json
{
  "token_fcm": "FCM_DEVICE_TOKEN"
}
```

Para borrarlo en logout:

```http
DELETE /appUsers/{id}/token-fcm
```

## Recomendación Flutter

Al tocar la notificación, usar `message.data["document_type"]`, `message.data["document_id"]` y `message.data["equipment_id"]` para navegar directo a la pantalla del documento.

## Base técnica usada de Firebase

La implementación sigue el patrón recomendado por la documentación oficial:

- Envío desde servidor con Firebase Admin SDK.
- Mensajes con `notification` y `data`.
- `data` solo con pares clave-valor string.
- Target por token de dispositivo.