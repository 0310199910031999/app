# API Asociar FOPC02 a Documento/File - Contexto para Frontend

## Resumen

Permite asociar un FOPC02 que fue creado sin documento (desde el menú CreateDocuments) con un documento existente (FO-SP-01, FO-SC-01, FO-OS-01). El `file_id` se obtiene automáticamente del documento seleccionado (puede ser null si el documento no tiene file).

---

## Endpoint 1: Obtener FOPC02 disponibles para vinculación

```http
GET /fopc02/available/{equipment_id}
```

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| equipment_id | number | ID del equipo |

### Criterio de disponibilidad

Un FOPC02 aparece en la lista si **no tiene documento asociado** (`fopc_services_id IS NULL`). Esto significa que nunca ha sido vinculado a un FO-SP-01, FO-SC-01 o FO-OS-01.

### Response 200

```json
[
  {
    "id": 15,
    "employee_name": "Juan Pérez",
    "date_created": "2026-08-01T10:30:00",
    "status": "Abierto"
  },
  {
    "id": 18,
    "employee_name": "Carlos López",
    "date_created": "2026-08-03T14:15:00",
    "status": "Abierto"
  }
]
```

### Response 200 (vacío)

```json
[]
```

---

## Endpoint 2: Asociar FOPC02 a documento

```http
PUT /fopc02/assign_document/{fopc02_id}
Content-Type: application/json
```

### Parámetros de URL

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| fopc02_id | number | ID del FOPC02 a asociar |

### Body

```json
{
  "document_type": "fosp01",
  "document_id": 42
}
```

### Campos del Body

| Campo | Tipo | Obligatorio | Valores permitidos | Descripción |
|-------|------|-------------|-------------------|-------------|
| document_type | string | ✅ | `fosp01`, `fosc01`, `foos01` | Tipo de documento a vincular |
| document_id | number | ✅ | - | ID del documento |

### Response 200

```json
// Si el documento tiene file
{
  "result": true,
  "message": "FOPC02 asociado exitosamente al documento FOSP01 #42 con file DALM2608001"
}

// Si el documento NO tiene file
{
  "result": true,
  "message": "FOPC02 asociado exitosamente al documento FOSP01 #42 (sin file asociado)"
}
```

### Response 400 (errores de validación)

```json
// FOPC02 no existe
{ "detail": "FOPC02 con ID 15 no encontrado" }

// Documento no existe
{ "detail": "Documento fosp01 con ID 42 no encontrado" }

// document_type inválido
{ "detail": "document_type inválido: fxxx. Debe ser: fosp01, fosc01, foos01" }

// Documento es de otro equipo
{ "detail": "El documento pertenece a otro equipo" }
```

---

## Flujo de la interfaz

```
┌─────────────────────────────────────────────────────────┐
│  1. Usuario entra al detalle del equipo                 │
│  2. Llama GET /fopc02/available/{equipment_id}         │
│  3. Muestra lista de FOPC02 disponibles (sin documento) │
│     ┌─────────────────────────────────────────────┐     │
│     │ ☐ FO-PC-02 #15 - Juan Pérez - 01/08/2026   │     │
│     │ ☐ FO-PC-02 #18 - Carlos López - 03/08/2026 │     │
│     └─────────────────────────────────────────────┘     │
│  4. Usuario selecciona un FOPC02                        │
│  5. Muestra documentos del equipo (de otros endpoints)  │
│     ┌─────────────────────────────────────────────┐     │
│     │ ☐ FO-SP-01 #42 (File: DALM2608001)         │     │
│     │ ☐ FO-OS-01 #38 (File: DALM2608002)         │     │
│     │ ☐ FO-SC-01 #55 (File: sin file)            │     │
│     └─────────────────────────────────────────────┘     │
│  6. Usuario selecciona un documento                     │
│  7. Llama PUT /fopc02/assign_document/15                │
│     Body: { document_type: "fosp01", document_id: 42 }  │
│  8. Backend asocia FOPC02 con documento (y file si tiene)│
│  9. Refresca la lista                                   │
└─────────────────────────────────────────────────────────┘
```

## Notas importantes

1. El `file_id` NO se envía en el body, se obtiene del documento seleccionado
2. Si el documento no tiene file, el FOPC02 queda vinculado al documento pero sin file
3. Si el file del documento está cerrado, la asociación igual funciona (no se reabre)
4. Si el FOPC02 tiene FOPP02 vinculados, también se les actualiza el `file_id` (solo si el documento tiene file)
5. La validación de "mismo equipo" asegura que no se vincule un documento de otro equipo
6. Una vez vinculado, el FOPC02 ya NO aparece en la lista de disponibles (porque ahora tiene `fopc_services_id`)
