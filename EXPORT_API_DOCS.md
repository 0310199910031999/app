# Export API - Documentación para Integración

**Base URL**: `{BASE_URL}/exports`

> **Local**: `http://127.0.0.1:8000/exports`
> **Producción**: `http://ddg.com.mx/dashboard/exports` (ajustar según deploy)

---

## Flujo General

```
1. POST {BASE_URL}/exports/                      → Crea el job
2. GET  {BASE_URL}/exports/{job_id}/status        → Poll de progreso
3. POST {BASE_URL}/exports/{job_id}/download-link → Genera link temporal
4. GET  {BASE_URL}/exports/download/{token}       → Descarga el ZIP
```

---

## 1. Crear Exportación

**POST** `{BASE_URL}/exports/`

### Request Body

```json
{
  "client_id": 90,
  "equipment_id": null,
  "start_date": "2023-01-01",
  "end_date": "2030-12-31",
  "requesting_user_id": 70,
  "export_type": "both",
  "format_filters": {
    "fo-bc-01": false,
    "fo-cr-02": true,
    "fo-em-01": true,
    "fo-im-01": false,
    "fo-im-03": false,
    "fo-le-01": true,
    "fo-os-01": false,
    "fo-pc-02": false,
    "fo-pp-02": false,
    "fo-sc-01": true,
    "fo-sp-01": true
  }
}
```

### Campos

| Campo | Tipo | Requerido | Default | Descripción |
|---|---|---|---|---|
| `client_id` | int | Sí | - | ID del cliente |
| `equipment_id` | int/null | No | null | ID del equipo. `null` = todos los equipos del cliente |
| `start_date` | string | Sí | - | Fecha inicio `YYYY-MM-DD` |
| `end_date` | string | Sí | - | Fecha fin `YYYY-MM-DD` (debe ser >= start_date) |
| `requesting_user_id` | int | Sí | - | ID del usuario que solicita (recibe el correo) |
| `export_type` | string | No | `'both'` | `'pdf'`, `'excel'` o `'both'` |
| `format_filters` | object | Sí | - | Al menos un `true` |

### Formatos disponibles

```typescript
type FormatFilter =
  | 'fo-bc-01'  // Batería Cargador
  | 'fo-cr-02'  // Carta Responsiva
  | 'fo-em-01'  // Entrega de Materiales
  | 'fo-im-01'  // Inspección Montacargas
  | 'fo-im-03'  // Inspección Montacargas
  | 'fo-le-01'  // Orden de Levantamiento
  | 'fo-os-01'  // Otros Servicios
  | 'fo-pc-02'  // Propiedad del Cliente
  | 'fo-pp-02'  // Identificación Propiedad
  | 'fo-sc-01'  // Servicio Correctivo
  | 'fo-sp-01'; // Servicio Preventivo
```

### Tipos de exportación (`export_type`)

| Valor | Descripción |
|---|---|
| `'both'` | Genera PDFs y Excel (default) |
| `'pdf'` | Solo genera los PDFs |
| `'excel'` | Solo genera el Excel consolidado |

### Response (202 Accepted)

```json
{
  "job_id": "abc123-uuid",
  "status": "queued",
  "stage": "queued",
  "message": "Exportación encolada correctamente."
}
```

---

## 2. Consultar Estado

**GET** `{BASE_URL}/exports/{job_id}/status`

### Response (200)

```json
{
  "job_id": "abc123-uuid",
  "status": "processing",
  "stage": "rendering_pdfs",
  "progress_pct": 45,
  "processed_documents": 12,
  "total_documents": 25,
  "message": "Generando archivos PDF.",
  "download_ready": false,
  "expires_at": null,
  "download_url": null,
  "error_message": null
}
```

### Estados posibles (`status`)

| Estado | Significado |
|---|---|
| `queued` | En cola, esperando procesamiento |
| `processing` | En progreso |
| `completed` | Listo para descargar |
| `failed` | Falló (ver `error_message`) |
| `expired` | Link de descarga expirado |

### Etapas (`stage`)

```
queued → collecting → rendering_pdfs → building_excel → compressing → notifying → completed
```

### Cuándo poll

- Cada **3-5 segundos** hasta que `status` sea `completed`, `failed` o `expired`
- Cuando `download_ready: true`, proceder al paso 3

---

## 3. Generar Link de Descarga

**POST** `{BASE_URL}/exports/{job_id}/download-link`

> Solo llamar cuando `download_ready: true` en el status.

### Response (200)

```json
{
  "job_id": "abc123-uuid",
  "expires_at": "2026-08-04T17:00:00",
  "download_url": "http://127.0.0.1:8000/exports/download/abc123token"
}
```

### Errores

| HTTP | Causa |
|---|---|
| 404 | Job no existe |
| 409 | Job aún no está listo |
| 410 | ZIP expirado o no disponible |

---

## 4. Descargar ZIP

**GET** `{BASE_URL}/exports/download/{token}`

> El `token` viene del `download_url` del paso anterior.

- Retorna: `application/zip`
- Nombre del archivo: `export_{job_id}.zip`
- El token expira en `EXPORT_URL_TTL_MINUTES` (default: 1440 min = 24h)

---

## 5. Reintentar Exportación

**POST** `{BASE_URL}/exports/{job_id}/retry`

> Útil cuando un job falló o expiró.

### Response (202)

```json
{
  "job_id": "nuevo-uuid",
  "source_job_id": "uuid-original",
  "status": "queued",
  "stage": "queued",
  "message": "Exportación reenviada correctamente."
}
```

---

## 6. Listar Exportaciones

**GET** `{BASE_URL}/exports/`

### Query Params (todos opcionales)

| Param | Tipo | Default | Descripción |
|---|---|---|---|
| `client_id` | int | null | Filtrar por cliente |
| `equipment_id` | int | null | Filtrar por equipo |
| `requesting_user_id` | int | null | Filtrar por usuario solicitante |
| `limit` | int | 20 | Max 100 |

> **Lógica de filtrado**: Todos los parámetros son opcionales. Se aplican como **AND** solo los que se envíen. Si no se envía ningún filtro, retorna todos los exports del sistema.

### Ejemplos de filtrado

| Request | Resultado |
|---|---|
| `GET {BASE_URL}/exports/` | Todos los exports |
| `GET {BASE_URL}/exports/?client_id=90` | Exports del cliente 90 |
| `GET {BASE_URL}/exports/?equipment_id=201` | Exports del equipo 201 |
| `GET {BASE_URL}/exports/?requesting_user_id=70` | Exports solicitados por usuario 70 |
| `GET {BASE_URL}/exports/?client_id=90&equipment_id=201` | Exports del cliente 90 Y equipo 201 |
| `GET {BASE_URL}/exports/?client_id=90&requesting_user_id=70` | Exports del cliente 90 solicitados por usuario 70 |
| `GET {BASE_URL}/exports/?client_id=90&equipment_id=201&requesting_user_id=70` | Los tres filtros |
| `GET {BASE_URL}/exports/?client_id=90&limit=50` | Exports del cliente 90, max 50 resultados |

### Response

```json
{
  "items": [
    {
      "job_id": "abc123",
      "requested_by_user_id": 70,
      "client_id": 90,
      "equipment_id": null,
      "start_date": "2023-01-01",
      "end_date": "2030-12-31",
      "format_filters": { "fo-sp-01": true },
      "export_type": "both",
      "status": "completed",
      "stage": "completed",
      "progress_pct": 100,
      "processed_documents": 25,
      "total_documents": 25,
      "message": "La exportación está lista.",
      "download_ready": true,
      "expires_at": "2026-08-04T17:00:00",
      "error_message": null,
      "download_count": 2,
      "created_at": "2026-08-03T12:00:00",
      "started_at": "2026-08-03T12:00:05",
      "finished_at": "2026-08-03T12:01:30",
      "updated_at": "2026-08-03T12:01:30",
      "can_retry": false
    }
  ]
}
```

### Orden de resultados

- Por defecto: `created_at DESC` (más recientes primero)
- Si necesitas paginación: usar `limit` + offset (pendiente de implementar)

---

## Ejemplo TypeScript (Angular)

```typescript
interface ExportRequest {
  client_id: number;
  equipment_id?: number | null;
  start_date: string;
  end_date: string;
  requesting_user_id: number;
  format_filters: Record<FormatFilter, boolean>;
  export_type?: 'pdf' | 'excel' | 'both';
}

interface ExportJob {
  job_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'expired';
  stage: string;
  progress_pct: number;
  processed_documents: number;
  total_documents: number;
  download_ready: boolean;
  expires_at: string | null;
  error_message: string | null;
}

interface ExportListParams {
  client_id?: number;
  equipment_id?: number;
  requesting_user_id?: number;
  limit?: number;
}

// 1. Crear exportación
const createExport = (payload: ExportRequest) =>
  this.http.post<ExportJobResponse>('/exports/', payload);

// 2. Poll de estado
const getStatus = (jobId: string) =>
  this.http.get<ExportJob>(`/exports/${jobId}/status`);

// 3. Generar link
const getDownloadLink = (jobId: string) =>
  this.http.post<DownloadLink>(`/exports/${jobId}/download-link`, {});

// 4. Descargar (abrir en navegador o descargar como blob)
const downloadUrl = `${environment.apiUrl}/exports/download/${token}`;

// 5. Listar exportaciones con filtros
const listExports = (params: ExportListParams) => {
  const httpParams = new HttpParams();
  if (params.client_id) httpParams.set('client_id', params.client_id);
  if (params.equipment_id) httpParams.set('equipment_id', params.equipment_id);
  if (params.requesting_user_id) httpParams.set('requesting_user_id', params.requesting_user_id);
  if (params.limit) httpParams.set('limit', params.limit);
  return this.http.get<{ items: ExportJob[] }>('/exports/', { params: httpParams });
};

// Ejemplos de uso:
listExports({ client_id: 90 })                          // exports de un cliente
listExports({ client_id: 90, equipment_id: 201 })       // de un cliente + equipo
listExports({ requesting_user_id: 70, limit: 50 })      // de un usuario, max 50
listExports({})                                          // todos
```

## Ejemplo Flutter

```dart
// 1. Crear exportación
final response = await http.post(
  Uri.parse('$baseUrl/exports/'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'client_id': 90,
    'equipment_id': null,
    'start_date': '2023-01-01',
    'end_date': '2030-12-31',
    'requesting_user_id': 70,
    'export_type': 'both', // 'pdf', 'excel', o 'both'
    'format_filters': {'fo-sp-01': true, 'fo-sc-01': true},
  }),
);
final jobId = jsonDecode(response.body)['job_id'];

// 2. Poll cada 3 segundos
Timer.periodic(Duration(seconds: 3), (timer) async {
  final status = await http.get('$baseUrl/exports/$jobId/status');
  final job = jsonDecode(status.body);
  if (job['download_ready'] == true) {
    timer.cancel();
    // 3. Generar link
    final link = await http.post('$baseUrl/exports/$jobId/download-link');
    final url = jsonDecode(link.body)['download_url'];
    // 4. Abrir/descargar ZIP
    launch(url);
  }
});

// 5. Listar exportaciones con filtros
Future<List<dynamic>> listExports({
  int? clientId,
  int? equipmentId,
  int? requestingUserId,
  int limit = 20,
}) async {
  final params = <String, String>{};
  if (clientId != null) params['client_id'] = clientId.toString();
  if (equipmentId != null) params['equipment_id'] = equipmentId.toString();
  if (requestingUserId != null) params['requesting_user_id'] = requestingUserId.toString();
  params['limit'] = limit.toString();

  final response = await http.get(
    Uri.parse('$baseUrl/exports/').replace(queryParameters: params),
  );
  return jsonDecode(response.body)['items'];
}

// Ejemplos de uso:
await listExports(clientId: 90);                    // exports de un cliente
await listExports(clientId: 90, equipmentId: 201);  // de un cliente + equipo
await listExports(requestingUserId: 70, limit: 50); // de un usuario, max 50
await listExports();                                 // todos
```

---

## Casos de Uso Comunes (Frontend)

### Historial de exports de un cliente (vista cliente)
```
GET {BASE_URL}/exports/?client_id={id}&limit=20
```

### Historial de exports de un equipo específico
```
GET {BASE_URL}/exports/?equipment_id={id}&limit=20
```

### Mis exports (usuario logueado)
```
GET {BASE_URL}/exports/?requesting_user_id={id}&limit=20
```

### Verificar si hay exports pendientes de un cliente
```
GET {BASE_URL}/exports/?client_id={id}&limit=100
// Filtrar en frontend por status === 'queued' || status === 'processing'
```

---

## Contenido del ZIP

```
{equipo_a}/
  2024/
    Enero/
      FO-SP-01 Servicio Preventivo/
        01-01-2024 FO-SP-01 Servicio Preventivo 123.pdf
    Febrero/
      ...
{equipo_b}/
  ...
Reporte de Servicios - {nombre_cliente}.xlsx
```

### Excel

- Fila 1: Título "Reporte de Servicios"
- Fila 2: Nombre del cliente
- Fila 3: Fecha de generación
- Fila 4: Watermark DAL Dealer
- Fila 5: Headers con auto-filtros
- Fila 6+: Datos

### Columnas Excel

| Columna | Contenido |
|---|---|
| ID | ID del documento |
| Equipo | Nombre/economico del equipo |
| Fecha | Fecha del documento |
| Tipo de servicio / Nombre de Formato | FO-XX-XX + nombre |
| Servicios realizados | Lista con bullets (o N/A) |
| Desperfectos | Lista con bullets (o N/A) |
| Técnico / Empleado | Nombre del técnico |
| Nombre de Recepción del Servicio | Persona que recibe |

---

## Notas Importantes

- El `requesting_user_id` determina **quién recibe el correo** con el link de descarga
- El link expira en **24 horas** (configurable via `EXPORT_URL_TTL_MINUTES`)
- Solo documentos con status `CERRADO` se incluyen en la exportación
- Si `equipment_id` es `null`, se exportan **todos los equipos** del cliente
- El worker debe estar corriendo (`python shared/export_worker.py`) para procesar jobs
