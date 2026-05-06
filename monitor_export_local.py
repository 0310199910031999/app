import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date

from config import settings


DEFAULT_API_BASE_URL = 'http://127.0.0.1:8000'
DEFAULT_PAYLOAD = {
    'client_id': 90,
    'equipment_id': 201,
    'start_date': date(2023, 1, 1).isoformat(),
    'end_date': date(2030, 12, 31).isoformat(),
    'requesting_user_id': 70,
    'format_filters': {
        'fo-cr-02': True,
        'fo-em-01': True,
        'fo-im-01': True,
        'fo-im-03': True,
        'fo-le-01': True,
        'fo-os-01': True,
        'fo-pc-02': True,
        'fo-pp-02': True,
        'fo-sc-01': True,
        'fo-sp-01': True,
    },
}
TERMINAL_STATUSES = {'completed', 'failed', 'expired', 'deleted'}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Dispara y monitorea un export job en el API local.')
    parser.add_argument('--api-base-url', default=DEFAULT_API_BASE_URL)
    parser.add_argument('--poll-seconds', type=float, default=3.0)
    return parser.parse_args()


def request_json(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    body = json.dumps(payload).encode('utf-8') if payload is not None else None
    headers = {'Content-Type': 'application/json'} if payload is not None else {}
    request = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_body = response.read().decode('utf-8')
            return response.status, json.loads(response_body) if response_body else {}
    except urllib.error.HTTPError as exc:
        response_body = exc.read().decode('utf-8')
        detail = json.loads(response_body) if response_body else {'detail': str(exc)}
        return exc.code, detail


def log(message: str):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')


def main() -> int:
    args = parse_args()
    api_base_url = args.api_base_url.rstrip('/')
    configured_export_base_url = (settings.EXPORT_BASE_URL or '').rstrip('/')

    if configured_export_base_url and configured_export_base_url != api_base_url:
        log(
            'ADVERTENCIA: EXPORT_BASE_URL está configurado como '
            f"'{configured_export_base_url}' y el monitoreo apunta a '{api_base_url}'."
        )

    log(f'Creando export job en {api_base_url}/exports/')
    log(f'Payload: {json.dumps(DEFAULT_PAYLOAD, ensure_ascii=True)}')
    create_status, create_body = request_json('POST', f'{api_base_url}/exports/', DEFAULT_PAYLOAD)
    if create_status != 202:
        log(f'No se pudo crear el export job. HTTP {create_status}: {create_body}')
        return 1

    job_id = create_body['job_id']
    log(f'Job creado: {job_id}')

    last_snapshot = None
    while True:
        status_code, status_body = request_json('GET', f'{api_base_url}/exports/{job_id}/status')
        if status_code != 200:
            log(f'No se pudo consultar el status. HTTP {status_code}: {status_body}')
            return 1

        snapshot = (
            status_body.get('status'),
            status_body.get('stage'),
            status_body.get('progress_pct'),
            status_body.get('processed_documents'),
            status_body.get('total_documents'),
            status_body.get('message'),
            status_body.get('error_message'),
        )
        if snapshot != last_snapshot:
            log(
                'Estado: '
                f"status={status_body.get('status')} "
                f"stage={status_body.get('stage')} "
                f"progress={status_body.get('progress_pct')}% "
                f"docs={status_body.get('processed_documents')}/{status_body.get('total_documents')} "
                f"message={status_body.get('message')}"
            )
            last_snapshot = snapshot

        if status_body.get('status') in TERMINAL_STATUSES:
            if status_body.get('status') == 'completed':
                log('La exportación terminó correctamente.')
                log(
                    'El correo debería llegar con enlace base: '
                    f"{(configured_export_base_url or api_base_url)}/exports/download/<token>"
                )
                expires_at = status_body.get('expires_at')
                if expires_at:
                    log(f'Expira en: {expires_at}')
                return 0

            log(f'La exportación terminó en estado {status_body.get("status")}: {status_body}')
            return 1

        time.sleep(args.poll_seconds)


if __name__ == '__main__':
    sys.exit(main())